# ==============================================================================
# MD Marketing & Diseño — Backend/apps/crm/views.py
# ==============================================================================

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, CatalogoItem
from .serializers import ClienteSerializer, ClienteListSerializer, CatalogoItemSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de clientes.

    GET    /api/v1/crm/clientes/              → lista paginada
    POST   /api/v1/crm/clientes/              → crear cliente
    GET    /api/v1/crm/clientes/{id}/         → detalle
    PUT    /api/v1/crm/clientes/{id}/         → editar completo
    PATCH  /api/v1/crm/clientes/{id}/         → editar parcial
    DELETE /api/v1/crm/clientes/{id}/         → desactivar (soft delete)
    GET    /api/v1/crm/clientes/buscar_ruc/   → buscar por número de identificación
    """

    queryset           = Cliente.objects.all().select_related("creado_por")
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ["activo", "tipo_identificacion", "ciudad"]
    search_fields      = ["razon_social", "nombre_comercial", "numero_identificacion", "correo_electronico"]
    ordering_fields    = ["razon_social", "creado_en"]
    ordering           = ["razon_social"]

    def get_serializer_class(self):
        if self.action == "list":
            return ClienteListSerializer
        return ClienteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # Por defecto solo activos; ?todos=true incluye inactivos
        if self.request.query_params.get("todos") != "true":
            qs = qs.filter(activo=True)
        return qs

    def destroy(self, request, *args, **kwargs):
        """Soft delete — marca como inactivo en vez de borrar."""
        cliente = self.get_object()
        cliente.activo = False
        cliente.save(update_fields=["activo"])
        return Response(
            {"detail": f"Cliente '{cliente.razon_social}' desactivado correctamente."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="buscar_ruc")
    def buscar_ruc(self, request):
        """
        Búsqueda rápida por número de identificación.
        GET /api/v1/crm/clientes/buscar_ruc/?q=0912345678
        Usado en el formulario de nueva orden para autocompletar el cliente.
        """
        q = request.query_params.get("q", "").strip()
        if not q:
            return Response({"detail": "Parámetro 'q' requerido."}, status=400)

        clientes = Cliente.objects.filter(
            numero_identificacion__icontains=q,
            activo=True,
        )[:10]

        serializer = ClienteListSerializer(clientes, many=True)
        return Response(serializer.data)


class CatalogoItemViewSet(viewsets.ModelViewSet):
    """
    CRUD del catálogo de productos y servicios.

    GET  /api/v1/crm/catalogo/           → lista con filtro por naturaleza
    GET  /api/v1/crm/catalogo/?naturaleza=SVC_DIG  → solo servicios
    GET  /api/v1/crm/catalogo/?naturaleza=PROD_FIS → solo productos físicos
    """

    queryset           = CatalogoItem.objects.all()
    serializer_class   = CatalogoItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ["naturaleza", "activo", "tarifa_iva", "unidad_medida"]
    search_fields      = ["codigo", "nombre", "descripcion"]
    ordering_fields    = ["codigo", "nombre", "precio_base_unitario"]
    ordering           = ["naturaleza", "nombre"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("todos") != "true":
            qs = qs.filter(activo=True)
        return qs