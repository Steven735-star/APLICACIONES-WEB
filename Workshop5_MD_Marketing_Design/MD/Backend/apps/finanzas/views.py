# ==============================================================================
# MD Marketing & Diseño — apps/finanzas/views.py
# ==============================================================================

import logging
from datetime import date
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.crm.models import Transaccion, CategoriaFinanciera
from apps.finanzas.reportes import (
    calcular_utilidad_neta,
    calcular_balance_iva,
    egresos_por_categoria,
    tendencia_mensual,
    conteo_ordenes_por_estado,
)
from .serializers import TransaccionSerializer, CategoriaFinancieraSerializer

logger = logging.getLogger("apps")


def _parsear_fechas(request):
    """Extrae fecha_inicio y fecha_fin del query string. Defecto: mes actual."""
    hoy        = date.today()
    primer_dia = hoy.replace(day=1)
    try:
        fecha_inicio = date.fromisoformat(
            request.query_params.get("fecha_inicio", primer_dia.isoformat())
        )
        fecha_fin = date.fromisoformat(
            request.query_params.get("fecha_fin", hoy.isoformat())
        )
    except ValueError:
        raise ValueError("Formato inválido. Use YYYY-MM-DD.")
    if fecha_inicio > fecha_fin:
        raise ValueError("fecha_inicio no puede ser mayor que fecha_fin.")
    return fecha_inicio, fecha_fin


class CategoriaFinancieraViewSet(viewsets.ModelViewSet):
    queryset           = CategoriaFinanciera.objects.all()
    serializer_class   = CategoriaFinancieraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields   = ["tipo", "activa"]
    search_fields      = ["codigo", "nombre"]


class TransaccionViewSet(viewsets.ModelViewSet):
    """
    Libro Mayor — CRUD de ingresos y egresos.
    DELETE implementa contra-asiento (no borra físicamente).
    """
    queryset = (
        Transaccion.objects
        .select_related("categoria", "orden", "cliente", "registrado_por")
        .order_by("-fecha_emision", "-fecha_registro")
    )
    serializer_class   = TransaccionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ["tipo", "anulada", "metodo_pago", "categoria", "cliente"]
    search_fields      = ["referencia", "descripcion", "cliente__razon_social"]
    ordering_fields    = ["fecha_emision", "monto_flujo_caja"]

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Anula la transacción con un contra-asiento. No DELETE físico."""
        from django.db import transaction as db_transaction
        from django.utils import timezone

        original = self.get_object()
        if original.anulada:
            return Response(
                {"detail": "Esta transacción ya está anulada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with db_transaction.atomic():
            original.anulada = True
            original.save(update_fields=["anulada"])

            Transaccion.objects.create(
                referencia          = f"ANUL-{original.referencia}",
                tipo                = original.tipo,
                categoria           = original.categoria,
                descripcion         = f"ANULACIÓN de {original.referencia}: {original.descripcion}",
                orden               = original.orden,
                cliente             = original.cliente,
                monto_neto          = -original.monto_neto,
                base_iva            = -original.base_iva,
                tarifa_iva_aplicada = original.tarifa_iva_aplicada,
                monto_iva           = -original.monto_iva,
                retencion_fuente    = -original.retencion_fuente,
                retencion_iva       = -original.retencion_iva,
                metodo_pago         = original.metodo_pago,
                fecha_emision       = timezone.now().date(),
                registrado_por      = request.user,
                transaccion_origen  = original,
            )

        logger.info(f"Transacción {original.referencia} anulada por {request.user.username}")
        return Response(
            {"detail": f"Transacción {original.referencia} anulada con contra-asiento."},
            status=status.HTTP_200_OK,
        )


class ReporteUtilidadView(APIView):
    """
    GET /api/v1/finanzas/reportes/utilidad/
    Parámetros opcionales: fecha_inicio, fecha_fin (YYYY-MM-DD)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            fi, ff = _parsear_fechas(request)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        r = calcular_utilidad_neta(fi, ff)
        return Response({
            "periodo":           {"inicio": fi, "fin": ff},
            "ingresos_brutos":   str(r["ingresos_brutos"]),
            "egresos_totales":   str(r["egresos_totales"]),
            "utilidad_neta":     str(r["utilidad_neta"]),
            "margen_porcentaje": r["margen_porcentaje"],
        })


class ReporteIVAView(APIView):
    """
    GET /api/v1/finanzas/reportes/iva/
    Balance técnico IVA para la declaración SRI (Form. 104).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            fi, ff = _parsear_fechas(request)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        r = calcular_balance_iva(fi, ff)
        return Response({
            "periodo":                       {"inicio": fi, "fin": ff},
            "iva_ventas":                    str(r["iva_ventas"]),
            "iva_compras":                   str(r["iva_compras"]),
            "retenciones_iva_recibidas":     str(r["retenciones_iva_recibidas"]),
            "retenciones_fuente_recibidas":  str(r["retenciones_fuente_recibidas"]),
            "saldo_iva":                     str(r["saldo_iva"]),
            "a_pagar_sri":                   r["a_pagar_sri"],
        })


class ReporteTendenciaView(APIView):
    """
    GET /api/v1/finanzas/reportes/tendencia/?anio=2024
    Serie mensual de ingresos, egresos y utilidad.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        anio  = int(request.query_params.get("anio", date.today().year))
        datos = tendencia_mensual(anio)
        return Response({
            "anio":  anio,
            "meses": [
                {
                    "mes":      row["mes"].strftime("%Y-%m"),
                    "ingresos": str(row["ingresos"]),
                    "egresos":  str(row["egresos"]),
                    "utilidad": str(row["utilidad"]),
                }
                for row in datos
            ],
        })


class ReporteEgresosView(APIView):
    """
    GET /api/v1/finanzas/reportes/egresos/
    Egresos agrupados por categoría, ordenados de mayor a menor.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            fi, ff = _parsear_fechas(request)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        datos = egresos_por_categoria(fi, ff)
        return Response({
            "periodo":    {"inicio": fi, "fin": ff},
            "categorias": [
                {
                    "codigo":      row["categoria__codigo"],
                    "nombre":      row["categoria__nombre"],
                    "total_neto":  str(row["total_neto"]),
                    "total_flujo": str(row["total_flujo"]),
                }
                for row in datos
            ],
        })


class DashboardResumenView(APIView):
    """
    GET /api/v1/finanzas/dashboard/
    KPIs del mes actual en una sola petición para el Dashboard React.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hoy        = date.today()
        primer_dia = hoy.replace(day=1)

        utilidad = calcular_utilidad_neta(primer_dia, hoy)
        iva      = calcular_balance_iva(primer_dia, hoy)
        ordenes  = conteo_ordenes_por_estado()

        return Response({
            "mes_actual": {"inicio": primer_dia, "fin": hoy},
            "finanzas": {
                "ingresos_brutos":   str(utilidad["ingresos_brutos"]),
                "egresos_totales":   str(utilidad["egresos_totales"]),
                "utilidad_neta":     str(utilidad["utilidad_neta"]),
                "margen_porcentaje": utilidad["margen_porcentaje"],
                "saldo_iva":         str(iva["saldo_iva"]),
                "a_pagar_sri":       iva["a_pagar_sri"],
            },
            "produccion": ordenes,
        })