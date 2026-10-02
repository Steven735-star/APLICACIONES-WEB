# ==============================================================================
# MD Marketing & Diseño — config/asgi.py
# Punto de entrada ASGI para el servidor en producción (Daphne / Uvicorn).
#
# Maneja DOS tipos de conexiones simultáneamente:
#   1. HTTP  → Django views y DRF endpoints (comportamiento estándar)
#   2. WS    → Django Channels (WebSockets para el Kanban en tiempo real)
#
# En desarrollo: `python manage.py runserver` usa esto automáticamente
#                gracias a `channels` en INSTALLED_APPS.
# En producción: `daphne -b 0.0.0.0 -p 8000 config.asgi:application`
# ==============================================================================

import os
import django
from django.core.asgi import get_asgi_application

# Establecer settings ANTES de importar cualquier módulo de Django.
# El worker Celery y Daphne usan esta variable para saber qué settings cargar.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

# Inicializar Django explícitamente antes de importar consumers y routing,
# ya que estos importan modelos que requieren que Django esté configurado.
django.setup()

# IMPORTANTE: estas importaciones van DESPUÉS de django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.auth import AuthMiddlewareStack               # noqa: E402
from channels.security.websocket import AllowedHostsOriginValidator  # noqa: E402
from apps.produccion.routing import websocket_urlpatterns  # noqa: E402


# ------------------------------------------------------------------------------
# Aplicación ASGI principal
#
# ProtocolTypeRouter decide qué handler usar según el tipo de protocolo:
#   - "http"      → Aplicación Django estándar (DRF, Admin, vistas)
#   - "websocket" → Django Channels con autenticación JWT
# ------------------------------------------------------------------------------

application = ProtocolTypeRouter(
    {
        # ── HTTP: Django estándar ──────────────────────────────────────────────
        "http": get_asgi_application(),

        # ── WebSocket: Django Channels ─────────────────────────────────────────
        # AllowedHostsOriginValidator: rechaza conexiones WS de orígenes no
        # incluidos en ALLOWED_HOSTS. Primera línea de defensa CSRF para WS.
        #
        # AuthMiddlewareStack: popula scope["user"] desde la sesión de Django
        # o desde el token JWT pasado en el query string:
        #   ws://localhost:8000/ws/kanban/?token=<access_token>
        #
        # URLRouter: mapea rutas WS a sus consumers (ver produccion/routing.py)
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
            )
        ),
    }
)


# ------------------------------------------------------------------------------
# REFERENCIA: rutas WebSocket disponibles
# Definidas en: apps/produccion/routing.py
#
#   ws://localhost:8000/ws/kanban/
#       → KanbanConsumer
#       → Emite evento cuando una Orden cambia de estado (post_transition FSM)
#       → Todos los clientes conectados reciben el update en tiempo real
#
# Protocolo de mensajes (JSON):
#   Cliente → Server:  { "type": "subscribe", "board": "all" }
#   Server  → Cliente: { "type": "orden.update", "orden_id": 42,
#                         "estado_anterior": "EN_DISENIO",
#                         "estado_nuevo": "EN_PRODUCCION",
#                         "numero_orden": "ORD-2024-00042",
#                         "cliente": "Empresa XYZ" }
# ------------------------------------------------------------------------------