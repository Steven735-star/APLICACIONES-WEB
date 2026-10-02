# ==============================================================================
# MD Marketing & Diseño — apps/crm/serializers.py
# ==============================================================================

from rest_framework import serializers
from .models import Cliente, CatalogoItem, TipoIdentificacion, NaturalezaItem


class ClienteListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listas — solo campos esenciales."""

    class Meta:
        model  = Cliente
        fields = [
            "id", "tipo_identificacion", "numero_identificacion",
            "razon_social", "nombre_comercial", "telefono_principal",
            "ciudad", "activo",
        ]


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer completo para crear/editar/ver detalle."""

    class Meta:
        model  = Cliente
        fields = "__all__"
        read_only_fields = ["creado_en", "actualizado", "creado_por"]

    def validate(self, data):
        tipo = data.get("tipo_identificacion")
        numero = data.get("numero_identificacion", "")

        # ------------------------------------------------------------------
        # Validación de coherencia entre tipo y número de identificación
        # ------------------------------------------------------------------

        if tipo == "CED":
            if len(numero) != 10:
                raise serializers.ValidationError({
                    "numero_identificacion":
                        "Una cédula debe tener exactamente 10 dígitos."
                })

        elif tipo == "RUC":
            if len(numero) != 13:
                raise serializers.ValidationError({
                    "numero_identificacion":
                        "Un RUC debe tener exactamente 13 dígitos."
                })

        # ------------------------------------------------------------------
        # Validación de retención
        # ------------------------------------------------------------------

        if (
            data.get("aplica_retencion_fuente")
            and not data.get("porcentaje_retencion_fuente")
        ):
            raise serializers.ValidationError({
                "porcentaje_retencion_fuente":
                    "Debe especificar el porcentaje si aplica retención."
            })
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["creado_por"] = request.user
        return super().create(validated_data)


class CatalogoItemSerializer(serializers.ModelSerializer):

    naturaleza_display    = serializers.CharField(source="get_naturaleza_display",    read_only=True)
    unidad_medida_display = serializers.CharField(source="get_unidad_medida_display", read_only=True)
    tarifa_iva_display    = serializers.CharField(source="get_tarifa_iva_display",    read_only=True)

    class Meta:
        model  = CatalogoItem
        fields = "__all__"
        read_only_fields = ["creado_en", "actualizado"]