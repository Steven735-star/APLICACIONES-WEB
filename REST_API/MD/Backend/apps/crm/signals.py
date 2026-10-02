# ==============================================================================
# MD Marketing & Diseño — Señales Django
# Automatizaciones críticas sin lógica en las vistas
# ==============================================================================

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_fsm.signals import post_transition   # Señal nativa de django-fsm

from .models import Orden, HistorialEstadoOrden


# ------------------------------------------------------------------------------
# 1. AUDIT TRAIL automático en cada transición de estado (FSM)
#    django-fsm emite post_transition con: sender, instance, name, source, target
# ------------------------------------------------------------------------------

@receiver(post_transition, sender=Orden)
def registrar_historial_estado(sender, instance, name, source, target, **kwargs):
    """
    Se ejecuta DESPUÉS de cada transición FSM exitosa.
    Crea un registro inmutable en HistorialEstadoOrden.
    El usuario activo se pasa via instance._usuario_activo (ver abajo).
    """
    usuario = getattr(instance, "_usuario_activo", None)
    HistorialEstadoOrden.objects.create(
        orden=instance,
        estado_anterior=source or "",
        estado_nuevo=target,
        cambiado_por=usuario,
    )


# ------------------------------------------------------------------------------
# 2. GENERADOR de número de orden correlativo y único
#    Formato: ORD-2024-00001
# ------------------------------------------------------------------------------

@receiver(post_save, sender=Orden)
def generar_numero_orden(sender, instance, created, **kwargs):
    if created and not instance.numero_orden:
        from django.utils import timezone
        anio = timezone.now().year
        # Conteo de órdenes del año actual (incluyendo la recién creada)
        correlativo = Orden.objects.filter(creado_en__year=anio).count()
        numero = f"ORD-{anio}-{correlativo:05d}"
        # UPDATE directo para evitar bucle de señales
        Orden.objects.filter(pk=instance.pk).update(numero_orden=numero)
        instance.numero_orden = numero


# ------------------------------------------------------------------------------
# CONVENCIÓN DE USO EN VISTAS/SERVICIOS:
#
#   def confirmar_pedido_view(request, orden_id):
#       orden = get_object_or_404(Orden, pk=orden_id)
#       orden._usuario_activo = request.user   # ← inyectar usuario
#       orden.confirmar_pedido()               # ← transición FSM
#       orden.save()                           # ← persiste el cambio de estado
#
# La señal post_transition captura _usuario_activo automáticamente.
# ------------------------------------------------------------------------------
