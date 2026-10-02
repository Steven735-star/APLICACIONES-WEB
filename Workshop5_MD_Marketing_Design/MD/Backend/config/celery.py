# ==============================================================================
# MD Marketing & Diseño — config/celery.py
# Configuración de la aplicación Celery.
#
# Este archivo se importa en config/__init__.py para que Celery
# quede disponible al iniciar Django: `from config.celery import app`
# ==============================================================================

import os
from celery import Celery
from celery.signals import setup_logging

# Apuntar a las settings correctas ANTES de instanciar Celery.
# El worker arranca con: DJANGO_SETTINGS_MODULE=settings.development celery -A config worker
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

# ------------------------------------------------------------------------------
# Instancia principal de Celery
# El nombre "md_marketing" identifica esta app en el broker (Redis)
# ------------------------------------------------------------------------------

app = Celery("md_marketing")

# Leer toda la configuración de Celery desde las Django settings.
# Todas las claves que empiezan con CELERY_ se mapean automáticamente.
# Ejemplo: CELERY_BROKER_URL → broker_url
app.config_from_object("django.conf:settings", namespace="CELERY")


# ------------------------------------------------------------------------------
# Autodescubrimiento de tareas
# Celery buscará un módulo `tasks.py` dentro de cada app en INSTALLED_APPS
# Y también buscará en el paquete `tasks/` de nivel raíz del proyecto.
# ------------------------------------------------------------------------------

app.autodiscover_tasks(
    packages=[
        "tasks",           # Backend/tasks/ (tareas_reportes, tareas_alertas, etc.)
        "apps.crm",        # Si en el futuro crm tiene sus propias tareas
        "apps.produccion", # Tareas de notificación de cambios de estado FSM
        "apps.finanzas",   # Generación de reportes PDF
        "apps.inventario", # Alertas de stock
    ]
)


# ------------------------------------------------------------------------------
# Tarea de debug — útil para verificar que el worker funcione
# Ejecutar con: celery -A config call config.celery.debug_task
# ------------------------------------------------------------------------------

@app.task(bind=True, name="config.celery.debug_task")
def debug_task(self):
    """Tarea de ping para verificar conectividad con el broker."""
    print(f"[Celery Debug] Request: {self.request!r}")
    return {"status": "ok", "worker": self.request.hostname}


# ------------------------------------------------------------------------------
# Señal: usar el sistema de logging de Django en el worker de Celery
# Evita que Celery sobreescriba la configuración de LOGGING en settings.py
# ------------------------------------------------------------------------------

@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


# ------------------------------------------------------------------------------
# REFERENCIA DE COMANDOS
# ------------------------------------------------------------------------------
#
# Iniciar worker (desarrollo):
#   celery -A config worker --loglevel=info --concurrency=2
#
# Iniciar Beat (tareas programadas):
#   celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#
# Ver tareas registradas:
#   celery -A config inspect registered
#
# Ver workers activos:
#   celery -A config inspect active
#
# Purgar cola de tareas pendientes:
#   celery -A config purge
#
# Flower (monitor web):
#   celery -A config flower --port=5555
# ------------------------------------------------------------------------------