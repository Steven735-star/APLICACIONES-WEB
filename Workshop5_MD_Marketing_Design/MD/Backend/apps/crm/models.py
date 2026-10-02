# ==============================================================================
# MD Marketing & Diseño — Sistema ERP/CRM
# Arquitectura de Modelos Django — Nivel Producción
# Autor: Arquitecto de Software Principal
# Base de Datos: PostgreSQL
# Dependencias externas: django-fsm, django-auditlog
# ==============================================================================

from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_fsm import FSMField, transition          # pip install django-fsm
from auditlog.registry import auditlog               # pip install django-auditlog


# ==============================================================================
# SECCIÓN 0 — UTILIDADES Y VALIDADORES
# ==============================================================================

def validar_identificacion_ecuador(valor: str) -> None:
    """
    Valida Cédula (10 dígitos) o RUC (13 dígitos) ecuatorianos.
    Implementa el algoritmo de módulo 10 del BCE/SRI.
    """
    valor = valor.strip()
    if not valor.isdigit():
        raise ValidationError(_("La identificación debe contener solo dígitos."))

    longitud = len(valor)
    if longitud not in (10, 13):
        raise ValidationError(
            _("Identificación inválida: debe tener 10 dígitos (Cédula) o 13 (RUC).")
        )

    # Provincia: primeros 2 dígitos deben estar entre 01 y 24, o 30 (extranjeros)
    provincia = int(valor[:2])
    if not (1 <= provincia <= 24 or provincia == 30):
        raise ValidationError(_("Código de provincia inválido en la identificación."))

    # Tercer dígito determina tipo de persona
    tercer_digito = int(valor[2])

    if tercer_digito < 6:
        # Persona Natural — módulo 10
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        digitos = [int(d) for d in valor[:9]]
        total = sum((d * c) - 9 if (d * c) > 9 else d * c for d, c in zip(digitos, coeficientes))
        verificador_calculado = (10 - (total % 10)) % 10
        if verificador_calculado != int(valor[9]):
            raise ValidationError(_("El dígito verificador de la cédula es incorrecto."))

    elif tercer_digito == 6:
        # Entidad Pública — módulo 11
        coeficientes = [3, 2, 7, 6, 5, 4, 3, 2]
        digitos = [int(d) for d in valor[:8]]
        total = sum(d * c for d, c in zip(digitos, coeficientes))
        residuo = total % 11
        verificador_calculado = 0 if residuo == 0 else 11 - residuo
        if verificador_calculado != int(valor[8]):
            raise ValidationError(_("El dígito verificador de entidad pública es incorrecto."))

    elif tercer_digito == 9:
        # Persona Jurídica/Sociedad — módulo 11
        coeficientes = [4, 3, 2, 7, 6, 5, 4, 3, 2]
        digitos = [int(d) for d in valor[:9]]
        total = sum(d * c for d, c in zip(digitos, coeficientes))
        residuo = total % 11
        verificador_calculado = 0 if residuo == 0 else 11 - residuo
        if verificador_calculado != int(valor[9]):
            raise ValidationError(_("El dígito verificador de persona jurídica es incorrecto."))
    else:
        raise ValidationError(_("Tercer dígito de identificación no reconocido."))

    # Para RUC: los últimos 3 dígitos deben ser > 000
    if longitud == 13 and int(valor[10:13]) == 0:
        raise ValidationError(_("El establecimiento del RUC no puede ser 000."))


# ==============================================================================
# SECCIÓN 1 — MÓDULO CRM: CLIENTES Y CONTACTOS
# ==============================================================================

class TipoIdentificacion(models.TextChoices):
    CEDULA      = "CED", _("Cédula")
    RUC         = "RUC", _("RUC")
    PASAPORTE   = "PAS", _("Pasaporte")


class Cliente(models.Model):
    """
    Entidad central del CRM. Representa a personas naturales o jurídicas.
    Un 'cliente' puede tener múltiples órdenes, historial de pagos y documentos.
    """
    # --- Identificación Fiscal ---
    tipo_identificacion = models.CharField(
        max_length=3,
        choices=TipoIdentificacion.choices,
        default=TipoIdentificacion.CEDULA,
    )
    numero_identificacion = models.CharField(
        max_length=13,
        unique=True,
        validators=[validar_identificacion_ecuador],
        error_messages={
            "unique": "Ya existe un cliente registrado con este número de identificación."
        },
        help_text=_("Cédula (10 dígitos) o RUC (13 dígitos)."),
    )

    # --- Datos Personales/Comerciales ---
    razon_social        = models.CharField(max_length=200, help_text=_("Nombre completo o razón social."))
    nombre_comercial    = models.CharField(max_length=200, blank=True)
    correo_electronico  = models.EmailField(blank=True)
    telefono_principal  = models.CharField(max_length=20, blank=True)
    telefono_secundario = models.CharField(max_length=20, blank=True)
    direccion           = models.TextField(blank=True)
    ciudad              = models.CharField(max_length=100, blank=True)

    # --- Configuración Fiscal por Defecto ---
    aplica_retencion_fuente = models.BooleanField(
        default=False,
        help_text=_("Marcar si este cliente es agente de retención."),
    )
    porcentaje_retencion_fuente = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"),
        help_text=_("Ej: 1.00 para 1%, 2.00 para 2%. Solo si aplica retención."),
    )

    # --- Control ---
    activo      = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="clientes_creados",
    )

    class Meta:
        verbose_name        = _("Cliente")
        verbose_name_plural = _("Clientes")
        ordering            = ["razon_social"]
        indexes             = [models.Index(fields=["numero_identificacion"])]

    def __str__(self):
        return f"{self.razon_social} [{self.numero_identificacion}]"


# ==============================================================================
# SECCIÓN 2 — CATÁLOGO DE PRODUCTOS Y SERVICIOS
# ==============================================================================

class NaturalezaItem(models.TextChoices):
    SERVICIO_DIGITAL = "SVC_DIG", _("Servicio Digital/Intangible")
    PRODUCTO_FISICO  = "PROD_FIS", _("Producto Físico/Manufactura")


class TarifaIVA(models.TextChoices):
    """
    Tarifas vigentes SRI Ecuador. Agregar nuevas tarifas sin romper datos históricos.
    """
    IVA_15  = "15.00", _("IVA 15%")
    IVA_0   = "0.00",  _("IVA 0% / Exento")
    IVA_5   = "5.00",  _("IVA 5% (bienes especiales)")


class UnidadMedida(models.TextChoices):
    UNIDAD    = "UND",   _("Unidad")
    MILLAR    = "MIL",   _("Millar")
    METRO2    = "M2",    _("Metro cuadrado")
    METRO_LIN = "ML",    _("Metro lineal")
    HORA      = "HR",    _("Hora")
    MES       = "MES",   _("Mes")
    GLOBAL    = "GLOB",  _("Global/Lote")


class CatalogoItem(models.Model):
    """
    Catálogo maestro de servicios y productos. Define el tipo, precio base y tarifa fiscal.
    Los OrderItem referencian aquí para heredar defaults configurables.
    """
    codigo      = models.CharField(max_length=30, unique=True)
    nombre      = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    naturaleza  = models.CharField(max_length=10, choices=NaturalezaItem.choices)
    unidad_medida = models.CharField(
        max_length=10, choices=UnidadMedida.choices, default=UnidadMedida.UNIDAD
    )
    tarifa_iva  = models.CharField(
        max_length=5, choices=TarifaIVA.choices, default=TarifaIVA.IVA_15
    )
    precio_base_unitario = models.DecimalField(
        max_digits=12, decimal_places=4,
        help_text=_("Precio de lista sin IVA. Puede sobreescribirse en el pedido."),
    )

    # Para productos físicos: activa cálculo por dimensiones
    requiere_dimensiones = models.BooleanField(
        default=False,
        help_text=_("Si True, el precio = precio_base * ancho_m * alto_m."),
    )

    activo      = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = _("Ítem de Catálogo")
        verbose_name_plural = _("Catálogo de Ítems")
        ordering            = ["naturaleza", "nombre"]

    def __str__(self):
        return f"[{self.codigo}] {self.nombre}"


# ==============================================================================
# SECCIÓN 3 — ÓRDENES DE TRABAJO (FSM)
# ==============================================================================

class EstadoOrden(models.TextChoices):
    """
    Máquina de estados finita (FSM) del ciclo de vida de una orden.
    Las transiciones válidas son controladas por django-fsm en la clase Orden.
    """
    COTIZADO         = "COTIZADO",          _("Cotizado")
    PENDIENTE_PAGO   = "PENDIENTE_PAGO",    _("Pendiente de Pago")
    EN_DISEÑO        = "EN_DISENIO",        _("En Diseño")
    EN_PRODUCCION    = "EN_PRODUCCION",     _("En Producción")
    LISTO_ENTREGA    = "LISTO_ENTREGA",     _("Listo para Entrega")
    ENTREGADO        = "ENTREGADO",         _("Entregado")
    CANCELADO        = "CANCELADO",         _("Cancelado")


class PrioridadOrden(models.TextChoices):
    NORMAL   = "NORMAL",   _("Normal")
    URGENTE  = "URGENTE",  _("Urgente")
    CRITICA  = "CRITICA",  _("Crítica / Express")


class Orden(models.Model):
    """
    Orden de Trabajo — entidad central del sistema operativo.
    Agrupa múltiples líneas (OrdenItem), controla el flujo FSM y genera
    los registros financieros al confirmarse el pago.
    """
    numero_orden = models.CharField(
        max_length=20, unique=True,
        help_text=_("Formato sugerido: ORD-YYYY-NNNNN. Generado automáticamente."),
    )
    cliente         = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ordenes")
    prioridad       = models.CharField(max_length=10, choices=PrioridadOrden.choices, default=PrioridadOrden.NORMAL)
    descripcion_general = models.TextField(blank=True)
    fecha_compromiso    = models.DateField(null=True, blank=True, help_text=_("Fecha prometida de entrega."))

    # --- FSM: Estado principal ---
    estado = FSMField(
        default=EstadoOrden.COTIZADO,
        choices=EstadoOrden.choices,
        protected=True,   # Impide modificación directa del campo; solo vía métodos FSM
    )

    # --- Totales calculados (DESNORMALIZACIÓN CONTROLADA) ---
    # NOTA: Estos campos son CACHES de presentación, nunca fuente de verdad financiera.
    # Se recalculan en el save() de OrdenItem. La verdad financiera vive en Transaccion.
    subtotal_neto   = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_iva       = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_orden     = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    # --- Control ---
    asignado_a  = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="ordenes_asignadas",
    )
    creado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        on_delete=models.SET_NULL, related_name="ordenes_creadas",
    )
    creado_en   = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    # ------------------------------------------------------------------ #
    #  TRANSICIONES FSM — Cada método es la ÚNICA forma de cambiar estado  #
    # ------------------------------------------------------------------ #

    @transition(
        field=estado,
        source=EstadoOrden.COTIZADO,
        target=EstadoOrden.PENDIENTE_PAGO,
    )
    def confirmar_pedido(self):
        """El cliente aprueba la cotización. Se espera pago o anticipo."""
        pass

    @transition(
        field=estado,
        source=EstadoOrden.PENDIENTE_PAGO,
        target=EstadoOrden.EN_DISEÑO,
    )
    def iniciar_disenio(self):
        """Pago recibido (total o anticipo acordado). Inicia fase creativa."""
        pass

    @transition(
        field=estado,
        source=EstadoOrden.EN_DISEÑO,
        target=EstadoOrden.EN_PRODUCCION,
    )
    def pasar_a_produccion(self):
        """Diseño aprobado por cliente. Entra a producción física/digital."""
        pass

    @transition(
        field=estado,
        source=EstadoOrden.EN_PRODUCCION,
        target=EstadoOrden.LISTO_ENTREGA,
    )
    def marcar_listo(self):
        """Producción terminada. Listo para entrega o envío."""
        pass

    @transition(
        field=estado,
        source=EstadoOrden.LISTO_ENTREGA,
        target=EstadoOrden.ENTREGADO,
    )
    def registrar_entrega(self):
        """Entrega física confirmada al cliente."""
        pass

    @transition(
        field=estado,
        source=[
            EstadoOrden.COTIZADO,
            EstadoOrden.PENDIENTE_PAGO,
            EstadoOrden.EN_DISEÑO,
        ],
        target=EstadoOrden.CANCELADO,
    )
    def cancelar(self):
        """Cancelación permitida sólo antes de iniciar producción."""
        pass

    # ------------------------------------------------------------------ #

    def recalcular_totales(self):
        """Agrega los totales desde las líneas de la orden. Llamar tras modificar ítems."""
        from django.db.models import Sum
        agg = self.items.aggregate(
            neto=Sum("monto_neto"),
            iva=Sum("monto_iva"),
            total=Sum("monto_total"),
        )
        self.subtotal_neto = agg["neto"] or Decimal("0.00")
        self.total_iva     = agg["iva"]  or Decimal("0.00")
        self.total_orden   = agg["total"] or Decimal("0.00")
        Orden.objects.filter(pk=self.pk).update(
            subtotal_neto=self.subtotal_neto,
            total_iva=self.total_iva,
            total_orden=self.total_orden,
        )

    class Meta:
        verbose_name        = _("Orden de Trabajo")
        verbose_name_plural = _("Órdenes de Trabajo")
        ordering            = ["-creado_en"]
        indexes             = [
            models.Index(fields=["estado"]),
            models.Index(fields=["cliente", "estado"]),
            models.Index(fields=["fecha_compromiso"]),
        ]

    def __str__(self):
        return f"{self.numero_orden} — {self.cliente} [{self.estado}]"


class HistorialEstadoOrden(models.Model):
    """
    Audit trail inmutable de cada transición FSM.
    Se crea automáticamente via señal post_transition de django-fsm.
    Nunca se modifica ni elimina (append-only).
    """
    orden           = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="historial_estados")
    estado_anterior = models.CharField(max_length=20, blank=True)
    estado_nuevo    = models.CharField(max_length=20)
    cambiado_por    = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    timestamp       = models.DateTimeField(auto_now_add=True)
    notas           = models.TextField(blank=True)

    class Meta:
        verbose_name        = _("Historial de Estado")
        verbose_name_plural = _("Historial de Estados")
        ordering            = ["timestamp"]
        # Tabla append-only: deshabilitar delete en admin y API
        default_permissions = ("view",)

    def __str__(self):
        return f"{self.orden.numero_orden}: {self.estado_anterior} → {self.estado_nuevo}"


# ==============================================================================
# SECCIÓN 4 — LÍNEAS DE ORDEN (OrdenItem)
# ==============================================================================

class OrdenItem(models.Model):
    """
    Línea de detalle de una Orden. Puede ser servicio digital o producto físico.
    Calcula su propio desglose fiscal al guardarse.
    """
    orden           = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="items")
    catalogo_item   = models.ForeignKey(
        CatalogoItem, on_delete=models.PROTECT, related_name="orden_items"
    )
    descripcion_personalizada = models.CharField(
        max_length=300, blank=True,
        help_text=_("Si difiere del catálogo, describe el trabajo específico."),
    )

    # --- Cantidad y Dimensiones ---
    cantidad    = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal("1.0000"),
        help_text=_("Unidades, metros², millares, etc."),
    )
    # Para productos con cálculo por área (lona, viniles, etc.)
    ancho_m     = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    alto_m      = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    # --- Precios (sin IVA) ---
    precio_unitario_neto = models.DecimalField(
        max_digits=12, decimal_places=4,
        help_text=_("Precio unitario SIN IVA. Copia el precio_base del catálogo pero es editable."),
    )
    descuento_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"),
        help_text=_("Descuento en porcentaje sobre el precio neto. Ej: 10.00 para 10%."),
    )

    # --- Impuestos (se calculan en save()) ---
    tarifa_iva  = models.CharField(
        max_length=5, choices=TarifaIVA.choices,
        help_text=_("Heredada del catálogo; modificable por ítem."),
    )

    # --- Montos calculados (redundantes pero necesarios para SQL directo y reportes) ---
    # Fórmula: monto_neto = precio_unitario_neto * cantidad_efectiva * (1 - descuento/100)
    # donde cantidad_efectiva = ancho_m * alto_m * cantidad (si requiere_dimensiones) else cantidad
    monto_neto  = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=Decimal("0.00"))
    monto_iva   = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=Decimal("0.00"))
    monto_total = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=Decimal("0.00"))

    orden_linea = models.PositiveSmallIntegerField(default=1, help_text=_("Orden visual en la cotización."))
    notas       = models.TextField(blank=True)

    class Meta:
        verbose_name        = _("Línea de Orden")
        verbose_name_plural = _("Líneas de Orden")
        ordering            = ["orden", "orden_linea"]
        constraints         = [
            models.UniqueConstraint(fields=["orden", "orden_linea"], name="uq_orden_linea_numero"),
        ]

    def calcular_montos(self):
        """Calcula monto_neto, monto_iva y monto_total desde las reglas de negocio."""
        if self.catalogo_item.requiere_dimensiones and self.ancho_m and self.alto_m:
            cantidad_efectiva = self.cantidad * self.ancho_m * self.alto_m
        else:
            cantidad_efectiva = self.cantidad

        neto_bruto = self.precio_unitario_neto * cantidad_efectiva
        descuento  = neto_bruto * (self.descuento_porcentaje / Decimal("100"))
        neto       = (neto_bruto - descuento).quantize(Decimal("0.01"))
        tasa_iva   = Decimal(self.tarifa_iva) / Decimal("100")
        iva        = (neto * tasa_iva).quantize(Decimal("0.01"))
        return neto, iva, (neto + iva)

    def save(self, *args, **kwargs):
        self.monto_neto, self.monto_iva, self.monto_total = self.calcular_montos()
        super().save(*args, **kwargs)
        # Recalcular totales en la orden padre (UPDATE atómico, sin cargar toda la orden)
        self.orden.recalcular_totales()

    def __str__(self):
        return f"L{self.orden_linea} — {self.catalogo_item.nombre} x{self.cantidad} [{self.orden.numero_orden}]"


# ==============================================================================
# SECCIÓN 5 — MOTOR FINANCIERO: LIBRO MAYOR (LEDGER)
# ==============================================================================

class TipoMovimiento(models.TextChoices):
    INGRESO = "ING", _("Ingreso")
    EGRESO  = "EGR", _("Egreso")


class CategoriaFinanciera(models.Model):
    """
    Plan de cuentas simplificado. Define categorías para ingresos y egresos.
    Ejemplos de egresos: Insumos, Tintas, Viniles, Sueldos, Servicios Básicos.
    """
    codigo      = models.CharField(max_length=20, unique=True)
    nombre      = models.CharField(max_length=100)
    tipo        = models.CharField(max_length=3, choices=TipoMovimiento.choices)
    descripcion = models.TextField(blank=True)
    activa      = models.BooleanField(default=True)

    class Meta:
        verbose_name        = _("Categoría Financiera")
        verbose_name_plural = _("Categorías Financieras")
        ordering            = ["tipo", "codigo"]

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} ({self.tipo})"


class MetodoPago(models.TextChoices):
    EFECTIVO        = "EFEC",   _("Efectivo")
    TRANSFERENCIA   = "TRANSF", _("Transferencia Bancaria")
    TARJETA_DEBITO  = "T_DEB",  _("Tarjeta de Débito")
    TARJETA_CREDITO = "T_CRED", _("Tarjeta de Crédito")
    CHEQUE          = "CHQ",    _("Cheque")
    OTRO            = "OTRO",   _("Otro")


class Transaccion(models.Model):
    """
    LIBRO MAYOR — Fuente absoluta de verdad financiera.
    Cada fila representa un flujo de dinero real (ingreso o egreso).
    INMUTABLE después de ser cerrada. Nunca DELETE; solo anulaciones
    con Transaccion de signo inverso (contra-asiento).

    Estructura fiscal SRI Ecuador:
    ┌─────────────────────────────────────────────────────────────┐
    │  monto_neto                                                 │
    │  + base_iva (monto sobre el que se aplica IVA ≠ 0)          │
    │  + monto_iva (base_iva × tarifa_iva / 100)                  │
    │  − retencion_fuente                                         │
    │  − retencion_iva                                            │
    │  = monto_flujo_caja  (dinero que realmente entra/sale)      │
    └─────────────────────────────────────────────────────────────┘
    """
    # --- Identificación ---
    referencia  = models.CharField(
        max_length=50, unique=True,
        help_text=_("Número de factura, recibo, egreso. Ej: FAC-2024-001."),
    )
    tipo        = models.CharField(max_length=3, choices=TipoMovimiento.choices)
    categoria   = models.ForeignKey(CategoriaFinanciera, on_delete=models.PROTECT)
    descripcion = models.TextField()

    # --- Relación Opcional con Orden ---
    orden       = models.ForeignKey(
        Orden, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="transacciones",
    )
    cliente     = models.ForeignKey(
        Cliente, null=True, blank=True,
        on_delete=models.PROTECT, related_name="transacciones",
    )

    # --- Desglose Fiscal (todos en USD, moneda Ecuador) ---
    monto_neto              = models.DecimalField(max_digits=14, decimal_places=2)
    base_iva                = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"),
        help_text=_("Porción del monto_neto gravada con IVA ≠ 0."),
    )
    tarifa_iva_aplicada     = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"),
        help_text=_("Tasa real aplicada. Ej: 15.00 o 0.00."),
    )
    monto_iva               = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"),
        help_text=_("= base_iva × tarifa_iva_aplicada / 100. Calculado automáticamente."),
    )
    retencion_fuente        = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"),
        help_text=_("Retención en la fuente aplicada por el cliente (si es ag. retención)."),
    )
    retencion_iva           = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"),
        help_text=_("Retención de IVA (30%, 70%, 100% del IVA según tipo de cliente)."),
    )
    # Campo calculado al guardar: el dinero que entra/sale del banco
    monto_flujo_caja        = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False,
        help_text=_("= monto_neto + monto_iva − ret_fuente − ret_iva."),
    )

    # --- Metadatos del Pago ---
    metodo_pago     = models.CharField(max_length=10, choices=MetodoPago.choices)
    fecha_emision   = models.DateField(help_text=_("Fecha del documento fiscal."))
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    # --- Anulación / Contra-asiento ---
    anulada         = models.BooleanField(default=False)
    transaccion_origen = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT,
        related_name="contra_asientos",
        help_text=_("Si esta transacción es un contra-asiento, apunta a la original."),
    )

    # --- Auditoría ---
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="transacciones_registradas",
    )

    def clean(self):
        # Verificar coherencia del IVA
        iva_calculado = (self.base_iva * self.tarifa_iva_aplicada / Decimal("100")).quantize(Decimal("0.01"))
        if abs(iva_calculado - self.monto_iva) > Decimal("0.05"):
            raise ValidationError({
                "monto_iva": _(
                    f"El IVA declarado ({self.monto_iva}) no coincide con el calculado "
                    f"({iva_calculado}) sobre la base {self.base_iva} a {self.tarifa_iva_aplicada}%."
                )
            })

    def save(self, *args, **kwargs):
        self.monto_flujo_caja = (
            self.monto_neto
            + self.monto_iva
            - self.retencion_fuente
            - self.retencion_iva
        )
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name        = _("Transacción Financiera")
        verbose_name_plural = _("Transacciones Financieras")
        ordering            = ["-fecha_emision", "-fecha_registro"]
        indexes             = [
            models.Index(fields=["tipo", "fecha_emision"]),
            models.Index(fields=["anulada", "tipo"]),
            models.Index(fields=["orden"]),
        ]
        # Clave de negocio: no puede haber dos facturas con el mismo número
        constraints         = [
            models.UniqueConstraint(fields=["referencia"], name="uq_transaccion_referencia"),
        ]

    def __str__(self):
        return f"[{self.tipo}] {self.referencia} — ${self.monto_flujo_caja}"


# ==============================================================================
# SECCIÓN 6 — MATERIA PRIMA E INVENTARIO (Para costos reales)
# ==============================================================================

class MateriaPrima(models.Model):
    """
    Insumos de producción: vinil, tinta, papel adhesivo, lona, etc.
    Se asocia a órdenes de egreso para calcular costo real de producción.
    """
    codigo          = models.CharField(max_length=30, unique=True)
    nombre          = models.CharField(max_length=150)
    unidad_medida   = models.CharField(max_length=10, choices=UnidadMedida.choices)
    stock_actual    = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal("0.0000"))
    stock_minimo    = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal("0.0000"),
        help_text=_("Alerta cuando el stock baje de este nivel."),
    )
    costo_unitario  = models.DecimalField(
        max_digits=12, decimal_places=4,
        help_text=_("Costo de compra por unidad, sin IVA."),
    )
    proveedor       = models.CharField(max_length=150, blank=True)
    activo          = models.BooleanField(default=True)

    class Meta:
        verbose_name        = _("Materia Prima")
        verbose_name_plural = _("Materias Primas")
        ordering            = ["nombre"]

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock_actual} {self.unidad_medida})"

    @property
    def alerta_stock(self) -> bool:
        return self.stock_actual <= self.stock_minimo


class ConsumoMateriaPrima(models.Model):
    """
    Registro de consumo de insumos por orden. Permite calcular el costo
    real de producción de cada trabajo para obtener margen neto real.
    """
    orden           = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="consumos")
    materia_prima   = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad        = models.DecimalField(max_digits=12, decimal_places=4)
    costo_unitario_momento = models.DecimalField(
        max_digits=12, decimal_places=4,
        help_text=_("Costo al momento del consumo (snapshot histórico)."),
    )
    costo_total     = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    registrado_en   = models.DateTimeField(auto_now_add=True)
    registrado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        self.costo_total = (self.cantidad * self.costo_unitario_momento).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
        # Descontar stock automáticamente
        MateriaPrima.objects.filter(pk=self.materia_prima_id).update(
            stock_actual=models.F("stock_actual") - self.cantidad
        )

    class Meta:
        verbose_name        = _("Consumo de Materia Prima")
        verbose_name_plural = _("Consumos de Materia Prima")


# ==============================================================================
# REGISTRO EN django-auditlog (trazabilidad completa a nivel de campo)
# ==============================================================================

auditlog.register(Cliente,      include_fields=["razon_social", "numero_identificacion", "activo"])
auditlog.register(Orden,        include_fields=["estado", "prioridad", "asignado_a", "fecha_compromiso"])
auditlog.register(OrdenItem)
auditlog.register(Transaccion,  include_fields=["anulada", "monto_flujo_caja", "referencia"])
auditlog.register(MateriaPrima, include_fields=["stock_actual", "costo_unitario"])
