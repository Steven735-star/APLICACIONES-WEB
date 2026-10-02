# ==============================================================================
# MD Marketing & Diseño — apps/inventario/serializers.py
# ==============================================================================

from rest_framework import serializers
from apps.crm.models import MateriaPrima, ConsumoMateriaPrima


class MateriaPrimaSerializer(serializers.ModelSerializer):
    alerta_stock          = serializers.BooleanField(read_only=True)
    unidad_medida_display = serializers.CharField(
        source="get_unidad_medida_display", read_only=True
    )

    class Meta:
        model  = MateriaPrima
        fields = "__all__"


class ConsumoMateriaPrimaSerializer(serializers.ModelSerializer):
    materia_prima_nombre = serializers.CharField(
        source="materia_prima.nombre", read_only=True
    )
    orden_numero = serializers.CharField(
        source="orden.numero_orden", read_only=True
    )

    class Meta:
        model   = ConsumoMateriaPrima
        fields  = "__all__"
        read_only_fields = ["costo_total", "registrado_en"]