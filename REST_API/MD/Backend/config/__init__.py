# ==============================================================================
# MD Marketing & Diseño — config/__init__.py
#
# Importar la instancia de Celery aquí garantiza que la app quede
# registrada cuando Django inicia, incluso antes de que se importen
# las tareas individuales. Esto es el patrón oficial de Django + Celery.
# ==============================================================================

from .celery import app as celery_app

__all__ = ("celery_app",)