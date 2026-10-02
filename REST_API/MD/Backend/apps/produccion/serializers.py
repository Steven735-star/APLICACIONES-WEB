# ==============================================================================
# MD Marketing & Diseño — apps/produccion/serializers.py
# ==============================================================================

from rest_framework import serializers
from apps.crm.models import (
    Orden, OrdenItem, HistorialEstadoOrden, EstadoOrden,
)


class OrdenItemSerializer(serializers.ModelSerializer):
    catalogo_item_nombre = serializers.CharField(source="catalogo_item.nombre", read_only=True)
    catalogo_item_codigo = serializers.CharField(source="catalogo_item.codigo", read_only=True)

    class Meta:
        model  = OrdenItem
        fields = [
            "id", "orden", "catalogo_item", "catalogo_item_nombre",
            "catalogo_item_codigo", "descripcion_personalizada",
            "cantidad", "ancho_m", "alto_m",
            "precio_unitario_neto", "descuento_porcentaje", "tarifa_iva",
            "monto_neto", "monto_iva", "monto_total",
            "orden_linea", "notas",
        ]
        read_only_fields = ["monto_neto", "monto_iva", "monto_total"]


class HistorialEstadoSerializer(serializers.ModelSerializer):
    cambiado_por_nombre  = serializers.CharField(source="cambiado_por.get_full_name", read_only=True)
    duracion_minutos     = serializers.SerializerMethodField()

    class Meta:
        model  = HistorialEstadoOrden
        fields = [
            "id", "estado_anterior", "estado_nuevo",
            "cambiado_por", "cambiado_por_nombre",
            "timestamp", "notas", "duracion_minutos",
        ]
        read_only_fields = fields

    def get_duracion_minutos(self, obj):
        anterior = (
            HistorialEstadoOrden.objects
            .filter(orden=obj.orden, timestamp__lt=obj.timestamp)
            .order_by("-timestamp")
            .first()
        )
        if anterior:
            delta = obj.timestamp - anterior.timestamp
            return round(delta.total_seconds() / 60, 1)
        return None


class OrdenListSerializer(serializers.ModelSerializer):
    """Versión ligera para la lista del Kanban — mínimos campos."""
    cliente_nombre = serializers.CharField(source="cliente.razon_social",         read_only=True)
    cliente_ruc    = serializers.CharField(source="cliente.numero_identificacion", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display",            read_only=True)
    dias_en_estado = serializers.SerializerMethodField()

    class Meta:
        model  = Orden
        fields = [
            "id", "numero_orden", "cliente", "cliente_nombre", "cliente_ruc",
            "estado", "estado_display", "prioridad", "total_orden",
            "fecha_compromiso", "creado_en", "dias_en_estado",
        ]

    def get_dias_en_estado(self, obj):
        from django.utils import timezone
        ultimo = (
            HistorialEstadoOrden.objects
            .filter(orden=obj)
            .order_by("-timestamp")
            .first()
        )
        if ultimo:
            return (timezone.now() - ultimo.timestamp).days
        return 0


class OrdenSerializer(serializers.ModelSerializer):
    """Serializer completo: ítems, historial y transiciones disponibles."""
    items                    = OrdenItemSerializer(many=True, read_only=True)
    historial_estados        = HistorialEstadoSerializer(many=True, read_only=True)
    cliente_nombre           = serializers.CharField(source="cliente.razon_social", read_only=True)
    estado_display           = serializers.CharField(source="get_estado_display",   read_only=True)
    transiciones_disponibles = serializers.SerializerMethodField()

    class Meta:
        model  = Orden
        fields = [
            "id", "numero_orden", "cliente", "cliente_nombre",
            "estado", "estado_display", "prioridad", "descripcion_general",
            "fecha_compromiso", "asignado_a",
            "subtotal_neto", "total_iva", "total_orden",
            "items", "historial_estados",
            "transiciones_disponibles",
            "creado_en", "actualizado",
        ]
        read_only_fields = [
            "numero_orden", "subtotal_neto", "total_iva",
            "total_orden", "creado_en", "actualizado",
        ]

    def get_transiciones_disponibles(self, obj):
        MAPA = {
            EstadoOrden.COTIZADO:       [{"accion": "confirmar_pedido",   "label": "Confirmar Pedido",           "color": "blue"}],
            EstadoOrden.PENDIENTE_PAGO: [{"accion": "iniciar_disenio",    "label": "Pago Recibido → Diseño",     "color": "green"}],
            EstadoOrden.EN_DISEÑO:      [{"accion": "pasar_a_produccion", "label": "Aprobar Diseño → Producción","color": "orange"}],
            EstadoOrden.EN_PRODUCCION:  [{"accion": "marcar_listo",       "label": "Marcar como Listo",          "color": "teal"}],
            EstadoOrden.LISTO_ENTREGA:  [{"accion": "registrar_entrega",  "label": "Registrar Entrega",          "color": "green"}],
            EstadoOrden.ENTREGADO:      [],
            EstadoOrden.CANCELADO:      [],
        }
        transiciones = list(MAPA.get(obj.estado, []))
        if obj.estado in [EstadoOrden.COTIZADO, EstadoOrden.PENDIENTE_PAGO, EstadoOrden.EN_DISEÑO]:
            transiciones.append({"accion": "cancelar", "label": "Cancelar Orden", "color": "red"})
        return transiciones


class TransicionSerializer(serializers.Serializer):
    """Payload del endpoint POST /ordenes/{id}/transicion/"""
    accion = serializers.ChoiceField(choices=[
        "confirmar_pedido", "iniciar_disenio", "pasar_a_produccion",
        "marcar_listo", "registrar_entrega", "cancelar",
    ])
    notas  = serializers.CharField(required=False, allow_blank=True, default="")