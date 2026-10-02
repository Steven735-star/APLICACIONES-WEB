# ==============================================================================
# MD Marketing & Diseño — apps/inventario/views.py
# ==============================================================================

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from apps.crm.models import MateriaPrima, ConsumoMateriaPrima
from .serializers import MateriaPrimaSerializer, ConsumoMateriaPrimaSerializer


class MateriaPrimaViewSet(viewsets.ModelViewSet):
    """
    CRUD de materias primas e insumos de producción.

    GET /api/v1/inventario/materias-primas/           → lista completa
    GET /api/v1/inventario/materias-primas/alertas/   → items bajo stock mínimo
    """
    queryset           = MateriaPrima.objects.all()
    serializer_class   = MateriaPrimaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ["activo", "unidad_medida"]
    search_fields      = ["nombre", "codigo", "proveedor"]
    ordering_fields    = ["nombre", "stock_actual", "costo_unitario"]
    ordering           = ["nombre"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("todos") != "true":
            qs = qs.filter(activo=True)
        return qs

    @action(detail=False, methods=["get"], url_path="alertas")
    def alertas(self, request):
        """
        Retorna todos los insumos cuyo stock_actual <= stock_minimo.
        Usado para el panel de alertas del dashboard.
        """
        criticos = MateriaPrima.objects.filter(
            activo=True,
            stock_actual__lte=F("stock_minimo"),
        ).order_by("nombre")

        serializer = self.get_serializer(criticos, many=True)
        return Response({
            "total_alertas": criticos.count(),
            "items": serializer.data,
        })

    @action(detail=True, methods=["post"], url_path="ajustar-stock")
    def ajustar_stock(self, request, pk=None):
        """
        Ajusta el stock manualmente (ej: inventario físico).
        POST /api/v1/inventario/materias-primas/{id}/ajustar-stock/
        Body: { "cantidad": 50.0, "motivo": "Inventario físico mensual" }
        """
        materia = self.get_object()
        cantidad = request.data.get("cantidad")
        motivo   = request.data.get("motivo", "Ajuste manual")

        if cantidad is None:
            return Response(
                {"detail": "El campo 'cantidad' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cantidad = float(cantidad)
        except (ValueError, TypeError):
            return Response(
                {"detail": "El campo 'cantidad' debe ser un número."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        stock_anterior = materia.stock_actual
        MateriaPrima.objects.filter(pk=materia.pk).update(
            stock_actual=F("stock_actual") + cantidad
        )
        materia.refresh_from_db()

        return Response({
            "nombre":         materia.nombre,
            "stock_anterior": str(stock_anterior),
            "ajuste":         str(cantidad),
            "stock_nuevo":    str(materia.stock_actual),
            "motivo":         motivo,
        })


class ConsumoMateriaPrimaViewSet(viewsets.ModelViewSet):
    """
    Registro de consumo de insumos por orden de producción.
    Al crear un consumo, el stock se descuenta automáticamente (via save()).
    """
    queryset = (
        ConsumoMateriaPrima.objects
        .select_related("orden", "materia_prima", "registrado_por")
        .order_by("-registrado_en")
    )
    serializer_class   = ConsumoMateriaPrimaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields   = ["orden", "materia_prima"]
    ordering_fields    = ["registrado_en", "costo_total"]

    def perform_create(self, serializer):
        serializer.save(
            registrado_por=self.request.user,
            costo_unitario_momento=serializer.validated_data["materia_prima"].costo_unitario,
        )

    def destroy(self, request, *args, **kwargs):
        """Los consumos no se borran — afectarían el historial de costos."""
        return Response(
            {"detail": "Los consumos no se pueden eliminar para preservar el historial de costos."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )