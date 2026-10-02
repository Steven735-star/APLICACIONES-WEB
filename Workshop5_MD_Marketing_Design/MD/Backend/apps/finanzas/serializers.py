# ==============================================================================
# MD Marketing & Diseño — apps/finanzas/serializers.py
# ==============================================================================

from decimal import Decimal
from rest_framework import serializers
from apps.crm.models import Transaccion, CategoriaFinanciera


class CategoriaFinancieraSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model  = CategoriaFinanciera
        fields = "__all__"


class TransaccionSerializer(serializers.ModelSerializer):
    tipo_display        = serializers.CharField(source="get_tipo_display",        read_only=True)
    metodo_pago_display = serializers.CharField(source="get_metodo_pago_display", read_only=True)
    categoria_nombre    = serializers.CharField(source="categoria.nombre",        read_only=True)
    cliente_nombre      = serializers.CharField(source="cliente.razon_social",    read_only=True)
    orden_numero        = serializers.CharField(source="orden.numero_orden",      read_only=True)

    class Meta:
        model   = Transaccion
        fields  = "__all__"
        read_only_fields = ["monto_flujo_caja", "fecha_registro"]

    def validate(self, data):
        base_iva  = data.get("base_iva",            Decimal("0.00"))
        tarifa    = data.get("tarifa_iva_aplicada", Decimal("0.00"))
        monto_iva = data.get("monto_iva",           Decimal("0.00"))

        calculado = (base_iva * tarifa / Decimal("100")).quantize(Decimal("0.01"))
        if abs(calculado - monto_iva) > Decimal("0.05"):
            raise serializers.ValidationError({
                "monto_iva": (
                    f"IVA declarado ({monto_iva}) ≠ calculado ({calculado}). "
                    f"Fórmula: {base_iva} × {tarifa}% / 100."
                )
            })
        return data