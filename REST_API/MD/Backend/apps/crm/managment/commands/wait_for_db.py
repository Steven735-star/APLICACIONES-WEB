# ==============================================================================
# MD Marketing & Diseño
# Backend/apps/crm/management/commands/wait_for_db.py
#
# Comando Django personalizado usado en el docker-compose.yml:
#   python manage.py wait_for_db
#
# Espera activamente hasta que PostgreSQL acepte conexiones antes
# de correr migraciones y levantar Daphne.
# Sin esto, Django arranca antes que la DB y falla con OperationalError.
#
# ESTRUCTURA DE CARPETAS NECESARIA:
#   Backend/apps/crm/management/__init__.py
#   Backend/apps/crm/management/commands/__init__.py
#   Backend/apps/crm/management/commands/wait_for_db.py   ← este archivo
# ==============================================================================

import time
import logging

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Espera a que la base de datos PostgreSQL esté disponible antes de continuar."

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Tiempo máximo de espera en segundos (default: 60)",
        )
        parser.add_argument(
            "--interval",
            type=float,
            default=1.0,
            help="Intervalo entre intentos en segundos (default: 1.0)",
        )

    def handle(self, *args, **options):
        timeout  = options["timeout"]
        interval = options["interval"]
        elapsed  = 0

        self.stdout.write("⏳ Esperando conexión con la base de datos...")

        while elapsed < timeout:
            try:
                # Intentar obtener la conexión default (PostgreSQL)
                conn = connections["default"]
                conn.ensure_connection()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Base de datos disponible (después de {elapsed:.1f}s)"
                    )
                )
                return

            except OperationalError:
                self.stdout.write(
                    f"   DB no disponible aún... reintentando en {interval}s "
                    f"({elapsed:.0f}/{timeout}s)"
                )
                time.sleep(interval)
                elapsed += interval

        # Si llegamos aquí, se agotó el tiempo
        self.stderr.write(
            self.style.ERROR(
                f"❌ Base de datos no disponible después de {timeout}s. "
                f"Verifica que el servicio 'db' está corriendo."
            )
        )
        raise SystemExit(1)