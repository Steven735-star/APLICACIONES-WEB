# ==============================================================================
# MD Marketing & Diseño — settings/development.py
# Sobreescribe settings/base.py para el entorno de desarrollo local.
# Activar con: DJANGO_SETTINGS_MODULE=settings.development
# ==============================================================================

from .base import *  # noqa: F401, F403

# ── Modo debug activado ────────────────────────────────────────────────────────
DEBUG = True

# En desarrollo, aceptar cualquier host
ALLOWED_HOSTS = ["*"]

# ── CORS: permitir el servidor de desarrollo de React ─────────────────────────
CORS_ALLOW_ALL_ORIGINS = True   # Solo en desarrollo local

# ── Base de datos local (puede ser SQLite para pruebas rápidas) ───────────────
# Para mantener PostgreSQL en desarrollo, usar docker-compose.
# Descomentar las siguientes líneas para usar SQLite sin Docker:
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# ── Herramientas de debug adicionales ─────────────────────────────────────────
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1", "::1"]

# ── Email: mostrar en consola en vez de enviar ────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ── Logging más detallado en desarrollo ───────────────────────────────────────
LOGGING["loggers"]["django.db.backends"]["level"] = "WARNING"
# Muestra cada query SQL ejecutada — útil para detectar N+1 queries

# ── DRF: habilitar Browsable API en desarrollo ────────────────────────────────
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += [  # noqa: F405
    "rest_framework.renderers.BrowsableAPIRenderer",
]


# ==============================================================================
# .env.example — copiar a .env y completar los valores
# ==============================================================================
#
# DJANGO_SECRET_KEY=django-insecure-cambia-esto-en-produccion-usa-50-chars-random
# DJANGO_DEBUG=True
# DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
# DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:5173 http://localhost:8000
# DJANGO_LOG_LEVEL=DEBUG
#
# # PostgreSQL
# POSTGRES_DB=md_marketing_db
# POSTGRES_USER=md_user
# POSTGRES_PASSWORD=md_secure_password_2024
# POSTGRES_HOST=db
# POSTGRES_PORT=5432
# DB_CONN_MAX_AGE=60
#
# # Redis
# REDIS_URL=redis://redis:6379
#
# # JWT
# JWT_ACCESS_MINUTES=60
# JWT_REFRESH_DAYS=7
#
# # CORS
# CORS_ALLOWED_ORIGINS=http://localhost:5173 http://localhost:3000
#
# # Email (producción)
# DEFAULT_FROM_EMAIL=noreply@mdmarketing.ec
# SERVER_EMAIL=errors@mdmarketing.ec
# # SMTP_HOST=smtp.tuproveedor.com
# # SMTP_PORT=587
# # SMTP_USER=tu@email.com
# # SMTP_PASSWORD=tu_password