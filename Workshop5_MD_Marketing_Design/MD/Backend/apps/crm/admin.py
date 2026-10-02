# ==============================================================================
# MD Marketing & Diseño — apps/crm/admin.py
# ==============================================================================

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Cliente, CatalogoItem,
    Orden, OrdenItem, HistorialEstadoOrden,
    Transaccion, CategoriaFinanciera,
    MateriaPrima, ConsumoMateriaPrima,
)


# ── CLIENTE ───────────────────────────────────────────────────────────────────

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display   = [
        "razon_social", "numero_identificacion", "tipo_identificacion",
        "telefono_principal", "ciudad", "activo",
    ]
    list_filter    = ["activo", "tipo_identificacion", "ciudad"]
    search_fields  = ["razon_social", "numero_identificacion", "correo_electronico"]
    ordering       = ["razon_social"]
    readonly_fields = ["creado_en", "actualizado", "creado_por"]
    fieldsets = (
        ("Identificación Fiscal", {
            "fields": ("tipo_identificacion", "numero_identificacion")
        }),
        ("Datos Comerciales", {
            "fields": ("razon_social", "nombre_comercial", "correo_electronico",
                       "telefono_principal", "telefono_secundario", "direccion", "ciudad")
        }),
        ("Configuración Fiscal", {
            "fields": ("aplica_retencion_fuente", "porcentaje_retencion_fuente")
        }),
        ("Control", {
            "fields": ("activo", "creado_por", "creado_en", "actualizado"),
            "classes": ("collapse",),
        }),
    )


# ── CATÁLOGO ──────────────────────────────────────────────────────────────────

@admin.register(CatalogoItem)
class CatalogoItemAdmin(admin.ModelAdmin):
    list_display   = [
        "codigo", "nombre", "naturaleza", "unidad_medida",
        "precio_base_unitario", "tarifa_iva", "requiere_dimensiones", "activo",
    ]
    list_filter    = ["naturaleza", "activo", "tarifa_iva", "unidad_medida"]
    search_fields  = ["codigo", "nombre", "descripcion"]
    ordering       = ["naturaleza", "nombre"]
    readonly_fields = ["creado_en", "actualizado"]


# ── ORDEN ─────────────────────────────────────────────────────────────────────

class OrdenItemInline(admin.TabularInline):
    model   = OrdenItem
    extra   = 1
    fields  = [
        "catalogo_item", "descripcion_personalizada", "cantidad",
        "ancho_m", "alto_m", "precio_unitario_neto",
        "descuento_porcentaje", "tarifa_iva",
        "monto_neto", "monto_iva", "monto_total",
    ]
    readonly_fields = ["monto_neto", "monto_iva", "monto_total"]


class HistorialEstadoInline(admin.TabularInline):
    model          = HistorialEstadoOrden
    extra          = 0
    readonly_fields = ["estado_anterior", "estado_nuevo", "cambiado_por", "timestamp", "notas"]
    can_delete     = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display    = [
        "numero_orden", "cliente", "estado_badge", "prioridad",
        "total_orden", "fecha_compromiso", "asignado_a",
    ]
    list_filter     = ["estado", "prioridad", "asignado_a"]
    search_fields   = ["numero_orden", "cliente__razon_social", "descripcion_general"]
    readonly_fields = ["numero_orden", "estado", "subtotal_neto", "total_iva", "total_orden", "creado_en", "actualizado"]
    inlines         = [OrdenItemInline, HistorialEstadoInline]
    ordering        = ["-creado_en"]
    fieldsets = (
        ("Identificación", {
            "fields": ("numero_orden", "cliente", "prioridad", "estado", "asignado_a")
        }),
        ("Detalles", {
            "fields": ("descripcion_general", "fecha_compromiso")
        }),
        ("Totales (calculados)", {
            "fields": ("subtotal_neto", "total_iva", "total_orden"),
            "classes": ("collapse",),
        }),
        ("Auditoría", {
            "fields": ("creado_en", "actualizado"),
            "classes": ("collapse",),
        }),
    )

    def estado_badge(self, obj):
        colores = {
            "COTIZADO":        "#6c757d",
            "PENDIENTE_PAGO":  "#fd7e14",
            "EN_DISENIO":      "#0d6efd",
            "EN_PRODUCCION":   "#6610f2",
            "LISTO_ENTREGA":   "#20c997",
            "ENTREGADO":       "#198754",
            "CANCELADO":       "#dc3545",
        }
        color = colores.get(obj.estado, "#6c757d")
        return format_html(
            '<span style="background:{};color:white;padding:3px 8px;border-radius:4px;font-size:11px">{}</span>',
            color, obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"


@admin.register(HistorialEstadoOrden)
class HistorialEstadoOrdenAdmin(admin.ModelAdmin):
    list_display    = ["orden", "estado_anterior", "estado_nuevo", "cambiado_por", "timestamp"]
    list_filter     = ["estado_nuevo"]
    readonly_fields = ["orden", "estado_anterior", "estado_nuevo", "cambiado_por", "timestamp", "notas"]
    ordering        = ["-timestamp"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ── FINANZAS ──────────────────────────────────────────────────────────────────

@admin.register(CategoriaFinanciera)
class CategoriaFinancieraAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "tipo", "activa"]
    list_filter  = ["tipo", "activa"]
    search_fields = ["codigo", "nombre"]


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display    = [
        "referencia", "tipo_badge", "categoria", "cliente_corto",
        "monto_neto", "monto_iva", "monto_flujo_caja",
        "metodo_pago", "fecha_emision", "anulada",
    ]
    list_filter     = ["tipo", "anulada", "metodo_pago", "categoria"]
    search_fields   = ["referencia", "descripcion", "cliente__razon_social"]
    readonly_fields = ["monto_flujo_caja", "fecha_registro"]
    ordering        = ["-fecha_emision"]
    fieldsets = (
        ("Identificación", {
            "fields": ("referencia", "tipo", "categoria", "descripcion")
        }),
        ("Relaciones", {
            "fields": ("orden", "cliente")
        }),
        ("Desglose Fiscal (SRI)", {
            "fields": (
                "monto_neto", "base_iva", "tarifa_iva_aplicada",
                "monto_iva", "retencion_fuente", "retencion_iva",
                "monto_flujo_caja",
            )
        }),
        ("Pago", {
            "fields": ("metodo_pago", "fecha_emision")
        }),
        ("Estado", {
            "fields": ("anulada", "transaccion_origen", "fecha_registro"),
            "classes": ("collapse",),
        }),
    )

    def tipo_badge(self, obj):
        color = "#198754" if obj.tipo == "ING" else "#dc3545"
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:11px">{}</span>',
            color, obj.get_tipo_display()
        )
    tipo_badge.short_description = "Tipo"

    def cliente_corto(self, obj):
        if obj.cliente:
            nombre = obj.cliente.razon_social
            return nombre[:25] + "…" if len(nombre) > 25 else nombre
        return "—"
    cliente_corto.short_description = "Cliente"

    def save_model(self, request, obj, form, change):
        if not obj.registrado_por:
            obj.registrado_por = request.user

        super().save_model(request, obj, form, change)


# ── INVENTARIO ────────────────────────────────────────────────────────────────

@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display  = [
        "nombre", "unidad_medida", "stock_actual",
        "stock_minimo", "costo_unitario", "alerta_stock_badge", "activo",
    ]
    list_filter   = ["activo", "unidad_medida"]
    search_fields = ["nombre", "codigo", "proveedor"]

    def alerta_stock_badge(self, obj):
        if obj.alerta_stock:
            return format_html(
                '<span style="background:#dc3545;color:white;padding:2px 8px;border-radius:4px;font-size:11px">⚠ BAJO MÍNIMO</span>'
            )
        return format_html(
            '<span style="background:#198754;color:white;padding:2px 8px;border-radius:4px;font-size:11px">OK</span>'
        )
    alerta_stock_badge.short_description = "Stock"


@admin.register(ConsumoMateriaPrima)
class ConsumoMateriaPrimaAdmin(admin.ModelAdmin):
    list_display    = ["orden", "materia_prima", "cantidad", "costo_unitario_momento", "costo_total", "registrado_en"]
    list_filter     = ["materia_prima"]
    readonly_fields = ["costo_total", "registrado_en"]
    search_fields   = ["orden__numero_orden", "materia_prima__nombre"]