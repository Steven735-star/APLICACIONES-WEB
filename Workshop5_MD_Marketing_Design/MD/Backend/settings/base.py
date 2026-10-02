# ==============================================================================
# MD Marketing & Diseño — settings/base.py
# Configuración base de Django. NO se usa directamente.
# Se hereda desde settings/development.py y settings/production.py
# ==============================================================================

import os
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured


# ------------------------------------------------------------------------------
# UTILIDAD: leer variables de entorno con error explícito si faltan
# ------------------------------------------------------------------------------

def env(key: str, default=None, required: bool = False) -> str:
    value = os.environ.get(key, default)
    if required and value is None:
        raise ImproperlyConfigured(
            f"La variable de entorno '{key}' es obligatoria y no está definida. "
            f"Agrégala al archivo .env"
        )
    return value


# ------------------------------------------------------------------------------
# RUTAS BASE
# ------------------------------------------------------------------------------

# Backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# SEGURIDAD
# ------------------------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY", required=True)

# SECURITY WARNING: En producción, DEBUG debe ser False.
# Controlado exclusivamente por variable de entorno.
DEBUG = env("DJANGO_DEBUG", default="False") == "True"

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", default="localhost 127.0.0.1").split()

# Protección CSRF para el Admin de Django
CSRF_TRUSTED_ORIGINS = env(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default="http://localhost:5173 http://localhost:8000"
).split()


# ------------------------------------------------------------------------------
# APLICACIONES INSTALADAS
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # API REST
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",

    # WebSockets (Kanban en tiempo real)
    "channels",

    # FSM para estados de Orden
    "django_fsm",

    # Auditoría a nivel de campo
    "auditlog",

    # CORS para React (Frontend en puerto distinto en desarrollo)
    "corsheaders",

    # Filtros avanzados en el ORM para la API
    "django_filters",
]

LOCAL_APPS = [
    "apps.crm.apps.CrmConfig",
    "apps.finanzas.apps.FinanzasConfig",
    "apps.produccion.apps.ProduccionConfig",
    "apps.inventario.apps.InventarioConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    # CORS debe ir primero, antes de cualquier middleware de Django
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Auditoría: registra el usuario en cada petición para django-auditlog
    "auditlog.middleware.AuditlogMiddleware",
]


# ------------------------------------------------------------------------------
# URLS Y WSGI / ASGI
# ------------------------------------------------------------------------------

ROOT_URLCONF     = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"   # Django Channels


# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ------------------------------------------------------------------------------
# BASE DE DATOS — PostgreSQL
# ------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     env("POSTGRES_DB",       required=True),
        "USER":     env("POSTGRES_USER",     required=True),
        "PASSWORD": env("POSTGRES_PASSWORD", required=True),
        "HOST":     env("POSTGRES_HOST",     default="db"),
        "PORT":     env("POSTGRES_PORT",     default="5432"),
        "CONN_MAX_AGE": int(env("DB_CONN_MAX_AGE", default="60")),
    }
}

# Auto-field por defecto para todos los modelos que no especifican PK
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ------------------------------------------------------------------------------
# CACHÉ — Redis
# Solo una instancia Redis, base de datos separadas por propósito:
#   DB 0: caché general
#   DB 1: sesiones Django
#   DB 2: Celery broker
#   DB 3: Django Channels layer
# ------------------------------------------------------------------------------

REDIS_URL = env("REDIS_URL", default="redis://redis:6379")

CACHES = {
    "default": {
        "BACKEND":  "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_URL}/0",
        "KEY_PREFIX": "md_erp",
        "TIMEOUT":    300,    # 5 minutos por defecto
    }
}

# Sesiones almacenadas en Redis (DB 1)
SESSION_ENGINE   = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# ------------------------------------------------------------------------------
# DJANGO CHANNELS — WebSockets (Kanban en tiempo real)
# ------------------------------------------------------------------------------

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"{REDIS_URL}/3"],
            "capacity":  1500,
            "expiry":    10,
        },
    },
}


# ------------------------------------------------------------------------------
# CELERY — Sistema de tareas distribuidas
# ------------------------------------------------------------------------------

CELERY_BROKER_URL              = f"{REDIS_URL}/2"
CELERY_RESULT_BACKEND          = f"{REDIS_URL}/2"
CELERY_ACCEPT_CONTENT          = ["json"]
CELERY_TASK_SERIALIZER         = "json"
CELERY_RESULT_SERIALIZER       = "json"
CELERY_TIMEZONE                = "America/Guayaquil"
CELERY_TASK_TRACK_STARTED      = True
CELERY_TASK_TIME_LIMIT         = 30 * 60          # 30 min máximo por tarea
CELERY_TASK_SOFT_TIME_LIMIT    = 25 * 60          # Warning a los 25 min
CELERY_WORKER_PREFETCH_MULTIPLIER = 1             # Evitar que un worker acapare tareas
CELERY_TASK_ACKS_LATE          = True             # Reconocer tarea solo si termina bien
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Autodescubrimiento de tareas: busca tasks.py en cada app LOCAL
CELERY_AUTODISCOVER_TASKS_PACKAGES = ["tasks"]

# Tareas programadas (Celery Beat)
from celery.schedules import crontab  # noqa: E402

CELERY_BEAT_SCHEDULE = {
    # Resumen financiero diario — 8:00 AM hora Ecuador
    "resumen-financiero-diario": {
        "task":     "tasks.tareas_programadas.generar_resumen_diario",
        "schedule": crontab(hour=8, minute=0),
    },
    # Alerta de órdenes con fecha de entrega vencida — cada 6 horas
    "alertas-ordenes-vencidas": {
        "task":     "tasks.tareas_alertas.verificar_ordenes_vencidas",
        "schedule": crontab(minute=0, hour="*/6"),
    },
    # Alerta de stock mínimo de materia prima — a las 7:30 AM
    "alerta-stock-minimo": {
        "task":     "tasks.tareas_alertas.verificar_stock_minimo",
        "schedule": crontab(hour=7, minute=30),
    },
    # Limpieza de tokens JWT en lista negra — cada domingo a las 2 AM
    "limpiar-tokens-jwt": {
        "task":     "tasks.tareas_programadas.limpiar_tokens_expirados",
        "schedule": crontab(hour=2, minute=0, day_of_week=0),
    },
}


# ------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Autenticación: JWT como método principal
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Por defecto, todos los endpoints requieren autenticación
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Paginación estándar para todas las listas
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    # Filtros, búsqueda y ordenamiento
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Throttling: protección contra abuso de la API
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "2000/day",
    },
    # Renderizadores: JSON en producción + BrowsableAPI en desarrollo
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Manejo de excepciones personalizable por app
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    # Formato de fecha/hora consistente con Ecuador
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
    "DATE_FORMAT":     "%Y-%m-%d",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "MD Marketing & Design API",
    "DESCRIPTION": (
        "REST API for the MD Marketing & Design system. "
        "Workshop 5 implementation demonstrating JWT authentication, "
        "protected resources, and CRUD operations."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
# ------------------------------------------------------------------------------
# JWT — Simple JWT
# ------------------------------------------------------------------------------

SIMPLE_JWT = {
    # Access token: corto para seguridad
    "ACCESS_TOKEN_LIFETIME":  timedelta(minutes=int(env("JWT_ACCESS_MINUTES",  default="60"))),
    # Refresh token: largo para UX sin re-login constante
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(env("JWT_REFRESH_DAYS",       default="7"))),
    "ROTATE_REFRESH_TOKENS":  True,   # Cada refresh emite nuevo refresh token
    "BLACKLIST_AFTER_ROTATION": True, # El refresh usado queda en lista negra
    "UPDATE_LAST_LOGIN":      True,
    "ALGORITHM":              "HS256",
    "SIGNING_KEY":            SECRET_KEY,
    "AUTH_HEADER_TYPES":      ("Bearer",),
    "AUTH_HEADER_NAME":       "HTTP_AUTHORIZATION",
    "USER_ID_FIELD":          "id",
    "USER_ID_CLAIM":          "user_id",
    "TOKEN_OBTAIN_SERIALIZER":  "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
}


# ------------------------------------------------------------------------------
# CORS — Cross-Origin Resource Sharing (para React en desarrollo)
# En producción: CORS_ALLOWED_ORIGINS reemplaza CORS_ALLOW_ALL_ORIGINS
# ------------------------------------------------------------------------------

# Se sobreescribe en development.py y production.py
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = env(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173 http://localhost:3000"
).split()

CORS_ALLOW_CREDENTIALS = True   # Necesario para enviar cookies/JWT

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


# ------------------------------------------------------------------------------
# INTERNACIONALIZACIÓN Y ZONA HORARIA — Ecuador
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "es-ec"
TIME_ZONE     = "America/Guayaquil"
USE_I18N      = True
USE_TZ        = True     # SIEMPRE True: fechas almacenadas en UTC, mostradas en TZ local


# ------------------------------------------------------------------------------
# ARCHIVOS ESTÁTICOS Y MEDIA
# ------------------------------------------------------------------------------

STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ------------------------------------------------------------------------------
# VALIDADORES DE CONTRASEÑA
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ------------------------------------------------------------------------------
# LOGGING — Estructura clara para desarrollo y producción
# ------------------------------------------------------------------------------

LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {process:d} {thread:d} — {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[{asctime}] {levelname} {name} — {message}",
            "style": "{",
            "datefmt": "%H:%M:%S",
        },
    },

    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true":  {"()": "django.utils.log.RequireDebugTrue"},
    },

    "handlers": {
        "console": {
            "level":     LOG_LEVEL,
            "class":     "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_error": {
            "level":     "ERROR",
            "class":     "logging.handlers.RotatingFileHandler",
            "filename":  BASE_DIR / "logs" / "errors.log",
            "maxBytes":  10 * 1024 * 1024,   # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filters":   ["require_debug_false"],
        },
        "file_general": {
            "level":     "INFO",
            "class":     "logging.handlers.RotatingFileHandler",
            "filename":  BASE_DIR / "logs" / "general.log",
            "maxBytes":  10 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "verbose",
        },
    },

    "loggers": {
        # Logger raíz de Django
        "django": {
            "handlers": ["console"],
            "level":    LOG_LEVEL,
            "propagate": True,
        },
        # Queries SQL lentas (> 200ms) — solo en desarrollo
        "django.db.backends": {
            "handlers": ["console"],
            "level":    "WARNING",
            "propagate": False,
        },
        # Nuestras aplicaciones
        "apps": {
            "handlers": ["console", "file_general", "file_error"],
            "level":    LOG_LEVEL,
            "propagate": False,
        },
        # Celery
        "celery": {
            "handlers": ["console", "file_general"],
            "level":    "INFO",
            "propagate": False,
        },
    },
}


# ------------------------------------------------------------------------------
# AUDITLOG — django-auditlog
# ------------------------------------------------------------------------------

# Los modelos se registran explícitamente con auditlog.register() en cada models.py
# No usamos INCLUDE_ALL_MODELS para tener control granular por modelo
AUDITLOG_INCLUDE_ALL_MODELS = False

# ------------------------------------------------------------------------------
# EMAIL (placeholder — sobreescribir en production.py con SMTP real)
# ------------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@mdmarketing.ec")
SERVER_EMAIL        = env("SERVER_EMAIL",       default="errors@mdmarketing.ec")


# ------------------------------------------------------------------------------
# MISCELÁNEA DE SEGURIDAD
# Se activan en production.py, se dejan neutros aquí para no romper desarrollo
# ------------------------------------------------------------------------------

SECURE_BROWSER_XSS_FILTER    = True
X_FRAME_OPTIONS              = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF  = True
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
