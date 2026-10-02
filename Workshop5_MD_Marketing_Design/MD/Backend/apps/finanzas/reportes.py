# ==============================================================================
# MD Marketing & Diseño — Motor de Reportes Financieros
# Consultas ORM Agregadas — Sin riesgo de desincronización
# Todas las cifras derivan EXCLUSIVAMENTE de la tabla Transaccion (Ledger)
# ==============================================================================

from decimal import Decimal
from django.db.models import (
    Sum, F, Q, Value, Case, When,
    DecimalField, ExpressionWrapper,
)
from django.db.models.functions import TruncMonth, TruncDay, Coalesce

from apps.crm.models import Transaccion, TipoMovimiento, ConsumoMateriaPrima, Orden


# ------------------------------------------------------------------------------
# UTILIDAD: Filtro base que excluye transacciones anuladas
# ------------------------------------------------------------------------------

def _transacciones_validas(fecha_inicio, fecha_fin):
    """Queryset base: período de fechas, sin anuladas."""
    return Transaccion.objects.filter(
        anulada=False,
        fecha_emision__gte=fecha_inicio,
        fecha_emision__lte=fecha_fin,
    )


# ==============================================================================
# 1. UTILIDAD NETA DEL PERÍODO
#    Ingreso real en caja − Egreso real en caja
# ==============================================================================

def calcular_utilidad_neta(fecha_inicio, fecha_fin) -> dict:
    """
    Retorna el P&L (Profit & Loss) del período solicitado.
    Fuente de verdad: campo monto_flujo_caja de cada Transaccion.

    Returns:
        {
          "ingresos_brutos":   Decimal,   # Suma flujo_caja de ING
          "egresos_totales":   Decimal,   # Suma flujo_caja de EGR (valor positivo)
          "utilidad_neta":     Decimal,   # ING − EGR
          "margen_porcentaje": float,     # (utilidad / ingresos) × 100
        }
    """
    qs = _transacciones_validas(fecha_inicio, fecha_fin)

    resultado = qs.aggregate(
        ingresos_brutos=Coalesce(
            Sum(
                "monto_flujo_caja",
                filter=Q(tipo=TipoMovimiento.INGRESO),
                output_field=DecimalField(),
            ),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        ),
        egresos_totales=Coalesce(
            Sum(
                "monto_flujo_caja",
                filter=Q(tipo=TipoMovimiento.EGRESO),
                output_field=DecimalField(),
            ),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        ),
    )

    ingresos = resultado["ingresos_brutos"]
    egresos  = resultado["egresos_totales"]
    utilidad = ingresos - egresos
    margen   = float(utilidad / ingresos * 100) if ingresos > 0 else 0.0

    return {
        "ingresos_brutos":   ingresos,
        "egresos_totales":   egresos,
        "utilidad_neta":     utilidad,
        "margen_porcentaje": round(margen, 2),
    }


# ==============================================================================
# 2. BALANCE TÉCNICO DE IVA (Crédito/Débito Fiscal — SRI Ecuador)
#    Para apoyo en la declaración mensual del Formulario 104
# ==============================================================================

def calcular_balance_iva(fecha_inicio, fecha_fin) -> dict:
    """
    IVA en Ventas (Débito Fiscal) vs IVA en Compras (Crédito Fiscal).
    El saldo positivo = IVA a pagar al SRI.
    El saldo negativo = crédito tributario a favor.

    Returns:
        {
          "iva_ventas":          Decimal,  # IVA cobrado en facturas de ingreso
          "iva_compras":         Decimal,  # IVA pagado en facturas de egreso
          "retenciones_iva_recibidas": Decimal,  # Retenciones que nos hicieron
          "saldo_iva":           Decimal,  # iva_ventas − iva_compras − ret_iva_recibidas
          "a_pagar_sri":         bool,
        }
    """
    qs = _transacciones_validas(fecha_inicio, fecha_fin)

    resultado = qs.aggregate(
        iva_ventas=Coalesce(
            Sum("monto_iva", filter=Q(tipo=TipoMovimiento.INGRESO)),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        ),
        iva_compras=Coalesce(
            Sum("monto_iva", filter=Q(tipo=TipoMovimiento.EGRESO)),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        ),
        retenciones_iva_recibidas=Coalesce(
            Sum("retencion_iva", filter=Q(tipo=TipoMovimiento.INGRESO)),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        ),
        retenciones_fuente_recibidas=Coalesce(
            Sum("retencion_fuente", filter=Q(tipo=TipoMovimiento.INGRESO)),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        ),
    )

    iva_v   = resultado["iva_ventas"]
    iva_c   = resultado["iva_compras"]
    ret_iva = resultado["retenciones_iva_recibidas"]
    saldo   = iva_v - iva_c - ret_iva

    return {
        "iva_ventas":                   iva_v,
        "iva_compras":                  iva_c,
        "retenciones_iva_recibidas":    ret_iva,
        "retenciones_fuente_recibidas": resultado["retenciones_fuente_recibidas"],
        "saldo_iva":                    saldo,
        "a_pagar_sri":                  saldo > Decimal("0.00"),
    }


# ==============================================================================
# 3. EGRESOS DESGLOSADOS POR CATEGORÍA
#    (Insumos, Sueldos, Servicios Básicos, etc.)
# ==============================================================================

def egresos_por_categoria(fecha_inicio, fecha_fin) -> list[dict]:
    """
    Desglosa los egresos por CategoríaFinanciera para identificar
    los mayores centros de costo del negocio.

    Returns: lista ordenada de dicts con categoria__nombre, total_egreso
    """
    return list(
        _transacciones_validas(fecha_inicio, fecha_fin)
        .filter(tipo=TipoMovimiento.EGRESO)
        .values("categoria__codigo", "categoria__nombre")
        .annotate(
            total_neto=Coalesce(Sum("monto_neto"), Value(Decimal("0.00")), output_field=DecimalField()),
            total_flujo=Coalesce(Sum("monto_flujo_caja"), Value(Decimal("0.00")), output_field=DecimalField()),
        )
        .order_by("-total_flujo")
    )


# ==============================================================================
# 4. TENDENCIA MENSUAL (Serie temporal para gráficos del Dashboard)
# ==============================================================================

def tendencia_mensual(anio: int) -> list[dict]:
    """
    Agrega ingresos y egresos por mes para el año dado.
    Útil para renderizar el gráfico de barras comparativo en el dashboard.

    Returns:
        [{"mes": date, "ingresos": Decimal, "egresos": Decimal, "utilidad": Decimal}, ...]
    """
    qs = (
        Transaccion.objects
        .filter(anulada=False, fecha_emision__year=anio)
        .annotate(mes=TruncMonth("fecha_emision"))
        .values("mes")
        .annotate(
            ingresos=Coalesce(
                Sum("monto_flujo_caja", filter=Q(tipo=TipoMovimiento.INGRESO)),
                Value(Decimal("0.00")), output_field=DecimalField(),
            ),
            egresos=Coalesce(
                Sum("monto_flujo_caja", filter=Q(tipo=TipoMovimiento.EGRESO)),
                Value(Decimal("0.00")), output_field=DecimalField(),
            ),
        )
        .annotate(
            utilidad=ExpressionWrapper(
                F("ingresos") - F("egresos"),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        )
        .order_by("mes")
    )
    return list(qs)


# ==============================================================================
# 5. RENTABILIDAD REAL POR ORDEN
#    Ingresos − Costo de Materiales consumidos = Margen Bruto
# ==============================================================================

def rentabilidad_por_orden(fecha_inicio, fecha_fin) -> list[dict]:
    """
    Por cada orden entregada en el período, calcula:
    - Ingreso cobrado (de Transaccion vinculada)
    - Costo de materia prima consumida
    - Margen bruto real

    Nota: Usa dos queries separadas y combina en Python para
    mantener el ORM legible y evitar JOINs complejos entre
    tablas con naturalezas distintas.
    """
    # 1. Ingresos por orden
    ingresos_qs = (
        Transaccion.objects
        .filter(
            anulada=False,
            tipo=TipoMovimiento.INGRESO,
            orden__isnull=False,
            fecha_emision__gte=fecha_inicio,
            fecha_emision__lte=fecha_fin,
        )
        .values("orden_id", "orden__numero_orden", "orden__cliente__razon_social")
        .annotate(
            ingreso_total=Coalesce(Sum("monto_flujo_caja"), Value(Decimal("0.00")), output_field=DecimalField())
        )
    )

    # 2. Costos de producción por orden
    costos_qs = (
        ConsumoMateriaPrima.objects
        .filter(orden__transacciones__fecha_emision__gte=fecha_inicio)
        .values("orden_id")
        .annotate(
            costo_materiales=Coalesce(Sum("costo_total"), Value(Decimal("0.00")), output_field=DecimalField())
        )
    )

    costos_dict = {row["orden_id"]: row["costo_materiales"] for row in costos_qs}

    resultado = []
    for row in ingresos_qs:
        ingreso  = row["ingreso_total"]
        costo    = costos_dict.get(row["orden_id"], Decimal("0.00"))
        margen   = ingreso - costo
        margen_p = float(margen / ingreso * 100) if ingreso > 0 else 0.0
        resultado.append({
            "orden_id":          row["orden_id"],
            "numero_orden":      row["orden__numero_orden"],
            "cliente":           row["orden__cliente__razon_social"],
            "ingreso_total":     ingreso,
            "costo_materiales":  costo,
            "margen_bruto":      margen,
            "margen_porcentaje": round(margen_p, 2),
        })

    return sorted(resultado, key=lambda x: x["margen_bruto"])


# ==============================================================================
# 6. DASHBOARD DE PRODUCCIÓN — Conteo de órdenes por estado (para Kanban)
# ==============================================================================

def conteo_ordenes_por_estado() -> dict:
    """
    Retorna un dict {estado: count} para renderizar el tablero Kanban.
    Un solo hit a la DB con GROUP BY.
    """
    from django.db.models import Count
    from apps.crm.models import EstadoOrden

    qs = (
        Orden.objects
        .values("estado")
        .annotate(total=Count("id"))
        .order_by("estado")
    )
    # Asegurar que todos los estados aparezcan aunque tengan 0
    base = {estado: 0 for estado in EstadoOrden.values}
    base.update({row["estado"]: row["total"] for row in qs})
    return base
