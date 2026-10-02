# ==============================================================================
# MD Marketing & Diseño — apps/produccion/views.py
# ==============================================================================

import logging
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_fsm import TransitionNotAllowed

from apps.crm.models import Orden, OrdenItem, EstadoOrden
from .serializers import (
    OrdenSerializer, OrdenListSerializer,
    OrdenItemSerializer, TransicionSerializer,
    HistorialEstadoSerializer,
)

logger = logging.getLogger("apps")

ACCIONES_FSM = {
    "confirmar_pedido":   "confirmar_pedido",
    "iniciar_disenio":    "iniciar_disenio",
    "pasar_a_produccion": "pasar_a_produccion",
    "marcar_listo":       "marcar_listo",
    "registrar_entrega":  "registrar_entrega",
    "cancelar":           "cancelar",
}


class OrdenViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Órdenes + transición FSM.

    GET    /api/v1/produccion/ordenes/                    → lista paginada
    POST   /api/v1/produccion/ordenes/                    → crear orden
    GET    /api/v1/produccion/ordenes/{id}/               → detalle completo
    PATCH  /api/v1/produccion/ordenes/{id}/               → editar
    POST   /api/v1/produccion/ordenes/{id}/transicion/    → cambiar estado
    GET    /api/v1/produccion/ordenes/{id}/historial/     → historial de estados
    """

    queryset = (
        Orden.objects
        .select_related("cliente", "asignado_a", "creado_por")
        .prefetch_related("items__catalogo_item", "historial_estados__cambiado_por")
        .order_by("-creado_en")
    )
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ["estado", "prioridad", "cliente", "asignado_a"]
    search_fields      = ["numero_orden", "cliente__razon_social", "descripcion_general"]
    ordering_fields    = ["creado_en", "fecha_compromiso", "total_orden"]

    def get_serializer_class(self):
        if self.action == "list":
            return OrdenListSerializer
        return OrdenSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(detail=True, methods=["post"], url_path="transicion")
    def transicion(self, request, pk=None):
        """
        Ejecuta una transición FSM sobre la orden.

        Body: { "accion": "confirmar_pedido", "notas": "..." }
        Retorna: la orden actualizada con el nuevo estado.
        Errores: 400 si la acción es inválida, 409 si la transición no está permitida.
        """
        orden      = self.get_object()
        serializer = TransicionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        accion = serializer.validated_data["accion"]
        notas  = serializer.validated_data.get("notas", "")
        metodo = getattr(orden, ACCIONES_FSM[accion])

        try:
            orden._usuario_activo = request.user
            metodo()
            orden.save()
            logger.info(
                f"[FSM] Orden {orden.numero_orden}: "
                f"'{accion}' por {request.user.username}"
            )
        except TransitionNotAllowed:
            return Response(
                {
                    "detail": (
                        f"Transición '{accion}' no permitida desde "
                        f"'{orden.get_estado_display()}'. "
                        f"Acciones disponibles: "
                        f"{[t['accion'] for t in OrdenSerializer(orden).data.get('transiciones_disponibles', [])]}"
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        # Actualizar notas en el historial recién creado por la señal
        if notas:
            ultimo = orden.historial_estados.order_by("-timestamp").first()
            if ultimo:
                ultimo.notas = notas
                ultimo.save(update_fields=["notas"])

        return Response(
            OrdenSerializer(orden, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="historial")
    def historial(self, request, pk=None):
        """Retorna el historial completo de transiciones de estado."""
        orden     = self.get_object()
        historial = (
            orden.historial_estados
            .select_related("cambiado_por")
            .order_by("timestamp")
        )
        return Response(HistorialEstadoSerializer(historial, many=True).data)


class KanbanView(APIView):
    """
    Datos del tablero Kanban — una sola petición para toda la UI.

    GET /api/v1/produccion/kanban/

    Retorna las órdenes activas agrupadas por estado,
    con conteo por columna para los headers del tablero.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.db.models import Count

        ESTADOS_ACTIVOS = [
            EstadoOrden.COTIZADO,
            EstadoOrden.PENDIENTE_PAGO,
            EstadoOrden.EN_DISEÑO,
            EstadoOrden.EN_PRODUCCION,
            EstadoOrden.LISTO_ENTREGA,
        ]

        ordenes = (
            Orden.objects
            .filter(estado__in=ESTADOS_ACTIVOS)
            .select_related("cliente")
            .order_by("prioridad", "fecha_compromiso")
        )

        conteos = dict(
            Orden.objects
            .filter(estado__in=ESTADOS_ACTIVOS)
            .values_list("estado")
            .annotate(total=Count("id"))
        )

        columnas = []
        for estado_val, estado_label in EstadoOrden.choices:
            if estado_val not in ESTADOS_ACTIVOS:
                continue
            ordenes_estado = [o for o in ordenes if o.estado == estado_val]
            columnas.append({
                "estado":   estado_val,
                "label":    estado_label,
                "total":    conteos.get(estado_val, 0),
                "ordenes":  OrdenListSerializer(ordenes_estado, many=True).data,
            })

        return Response({
            "columnas":      columnas,
            "total_activas": len(ordenes),
        })


class OrdenItemViewSet(viewsets.ModelViewSet):
    """CRUD de líneas de orden individuales."""
    queryset           = OrdenItem.objects.select_related("orden", "catalogo_item")
    serializer_class   = OrdenItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ["orden", "catalogo_item"]