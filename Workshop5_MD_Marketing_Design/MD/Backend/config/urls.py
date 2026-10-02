# ==============================================================================
# MD Marketing & Diseño — config/urls.py
# Router principal de la aplicación.
#
# Estructura de la API:
#   /admin/                     → Django Admin
#   /api/v1/auth/               → JWT (login, refresh, logout)
#   /api/v1/crm/                → Clientes, Catálogo
#   /api/v1/produccion/         → Órdenes, Items, Historial FSM
#   /api/v1/finanzas/           → Transacciones, Reportes
#   /api/v1/inventario/         → Materia Prima, Consumos
#   /api/v1/health/             → Health check (para Docker/load balancer)
# ==============================================================================
from apps.auth_views import current_user
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ------------------------------------------------------------------------------
# Health Check — endpoint liviano para Docker healthcheck y load balancers
# No requiere autenticación. Retorna 200 si Django y DB están operativos.
# ------------------------------------------------------------------------------

def health_check(request):
    """
    Verifica que Django responde y tiene conexión con la base de datos.
    Usado por docker-compose healthcheck y futuros load balancers.
    """
    from django.db import connection
    try:
        connection.ensure_connection()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    status_code = 200 if db_status == "ok" else 503
    return JsonResponse(
        {
            "status":    "ok" if db_status == "ok" else "degraded",
            "timestamp": timezone.now().isoformat(),
            "database":  db_status,
            "version":   "1.0.0",
        },
        status=status_code,
    )


# ------------------------------------------------------------------------------
# URL PATTERNS
# ------------------------------------------------------------------------------

urlpatterns = [
    # ── Admin de Django ────────────────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ── Health Check ───────────────────────────────────────────────────────────
    path("api/v1/health/", health_check, name="health-check"),

    # ── Autenticación JWT ──────────────────────────────────────────────────────
    # POST /api/v1/auth/token/          → Obtener access + refresh token
    # POST /api/v1/auth/token/refresh/  → Renovar access token
    # POST /api/v1/auth/token/blacklist/→ Logout (invalida refresh token)
    path(
        "api/v1/auth/",
        include("apps.auth_urls"),   # Archivo dedicado para endpoints JWT
    ),

    #
    path("api/v1/users/me/", current_user, name="current-user", ),

    # ── Módulo CRM ─────────────────────────────────────────────────────────────
    # /api/v1/crm/clientes/
    # /api/v1/crm/catalogo/
    path("api/v1/crm/", include("apps.crm.urls", namespace="crm")),

    # ── Módulo Producción (Órdenes + FSM + Kanban) ─────────────────────────────
    # /api/v1/produccion/ordenes/
    # /api/v1/produccion/ordenes/{id}/transicion/
    # /api/v1/produccion/kanban/
    path("api/v1/produccion/", include("apps.produccion.urls", namespace="produccion")),

    # ── Módulo Finanzas (Ledger + Reportes) ────────────────────────────────────
    # /api/v1/finanzas/transacciones/
    # /api/v1/finanzas/reportes/utilidad/
    # /api/v1/finanzas/reportes/iva/
    # /api/v1/finanzas/reportes/tendencia/
    path("api/v1/finanzas/", include("apps.finanzas.urls", namespace="finanzas")),

    # ── Módulo Inventario ──────────────────────────────────────────────────────
    # /api/v1/inventario/materias-primas/
    # /api/v1/inventario/consumos/
    path("api/v1/inventario/", include("apps.inventario.urls", namespace="inventario")),


# OpenAPI schema
path(
    "openapi/",
    SpectacularAPIView.as_view(),
    name="schema",
),

# Swagger UI
path(
    "docs/",
    SpectacularSwaggerView.as_view(url_name="schema"),
    name="swagger-ui",
),
]	
# ------------------------------------------------------------------------------
# ARCHIVOS ESTÁTICOS Y MEDIA en desarrollo
# En producción, Nginx sirve estos directorios directamente.
# ------------------------------------------------------------------------------

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django REST Framework Browsable API (solo en DEBUG)
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    ]


# ------------------------------------------------------------------------------
# CUSTOMIZACIÓN DEL ADMIN
# ------------------------------------------------------------------------------

admin.site.site_header  = "MD Marketing & Diseño — Panel de Administración"
admin.site.site_title   = "MD ERP/CRM"
admin.site.index_title  = "Panel de Control"


# ------------------------------------------------------------------------------
# APPS AUTH URLS — archivo auxiliar para JWT
# Crear como: Backend/apps/auth_urls.py
# ------------------------------------------------------------------------------
#
# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView,
# )
#
# urlpatterns = [
#     path("token/",           TokenObtainPairView.as_view(),   name="token_obtain_pair"),
#     path("token/refresh/",   TokenRefreshView.as_view(),      name="token_refresh"),
#     path("token/blacklist/", TokenBlacklistView.as_view(),    name="token_blacklist"),
# ]
# ------------------------------------------------------------------------------
