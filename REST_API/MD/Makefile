# ==============================================================================
# MD Marketing & Diseño — Makefile
# Comandos de desarrollo, base de datos, testing y mantenimiento.
#
# USO: make <comando>
# Ver todos los comandos: make help
# ==============================================================================

# Colores para output legible en terminal
RESET  := \033[0m
BOLD   := \033[1m
GREEN  := \033[32m
YELLOW := \033[33m
CYAN   := \033[36m
RED    := \033[31m
GRAY   := \033[90m

# Nombre del servicio Django en docker-compose
WEB     := web
CELERY  := celery
DB      := db
REDIS   := redis
DC      := docker compose

# Archivo de entorno
ENV_FILE := .env

.DEFAULT_GOAL := help

# ==============================================================================
# AYUDA — `make help` muestra todos los comandos disponibles
# ==============================================================================

.PHONY: help
help:
	@echo ""
	@echo "$(BOLD)$(CYAN)MD Marketing & Diseño — Comandos disponibles$(RESET)"
	@echo "$(GRAY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo ""
	@echo "$(BOLD)$(GREEN)🚀 ENTORNO$(RESET)"
	@echo "  $(CYAN)make dev$(RESET)              Levantar todos los servicios (modo desarrollo)"
	@echo "  $(CYAN)make build$(RESET)            Reconstruir imágenes Docker desde cero"
	@echo "  $(CYAN)make stop$(RESET)             Detener todos los servicios (preserva datos)"
	@echo "  $(CYAN)make restart$(RESET)          Reiniciar todos los servicios"
	@echo "  $(CYAN)make status$(RESET)           Ver estado de todos los contenedores"
	@echo ""
	@echo "$(BOLD)$(GREEN)🗄️  BASE DE DATOS$(RESET)"
	@echo "  $(CYAN)make migrate$(RESET)          Aplicar migraciones pendientes"
	@echo "  $(CYAN)make migrations$(RESET)       Generar nuevas migraciones (makemigrations)"
	@echo "  $(CYAN)make migrations-check$(RESET) Verificar si hay migraciones sin generar"
	@echo "  $(CYAN)make superuser$(RESET)        Crear superusuario administrador"
	@echo "  $(CYAN)make seed$(RESET)             Cargar datos iniciales (fixtures)"
	@echo "  $(CYAN)make db-shell$(RESET)         Abrir consola PostgreSQL (psql)"
	@echo "  $(CYAN)make db-backup$(RESET)        Exportar backup de la base de datos"
	@echo "  $(CYAN)make db-restore$(RESET)       Restaurar backup (uso: make db-restore FILE=backup.sql)"
	@echo "  $(CYAN)make flush$(RESET)            ⚠️  Borrar TODOS los datos (preserva tablas)"
	@echo ""
	@echo "$(BOLD)$(GREEN)🐚 CONSOLAS$(RESET)"
	@echo "  $(CYAN)make shell$(RESET)            Django shell interactivo (shell_plus si está instalado)"
	@echo "  $(CYAN)make bash$(RESET)             Bash dentro del contenedor web"
	@echo "  $(CYAN)make redis-cli$(RESET)        Consola Redis interactiva"
	@echo ""
	@echo "$(BOLD)$(GREEN)📋 LOGS$(RESET)"
	@echo "  $(CYAN)make logs$(RESET)             Logs en tiempo real de todos los servicios"
	@echo "  $(CYAN)make logs-web$(RESET)         Logs solo del servidor Django"
	@echo "  $(CYAN)make logs-celery$(RESET)      Logs de los workers Celery"
	@echo "  $(CYAN)make logs-db$(RESET)          Logs de PostgreSQL"
	@echo ""
	@echo "$(BOLD)$(GREEN)🧪 TESTING Y CALIDAD$(RESET)"
	@echo "  $(CYAN)make test$(RESET)             Ejecutar suite completa de tests (pytest)"
	@echo "  $(CYAN)make test-cov$(RESET)         Tests con reporte de cobertura HTML"
	@echo "  $(CYAN)make test-fast$(RESET)        Tests sin cobertura (más rápido)"
	@echo "  $(CYAN)make lint$(RESET)             Verificar estilo de código (flake8 + isort)"
	@echo "  $(CYAN)make format$(RESET)           Formatear código automáticamente (black + isort)"
	@echo "  $(CYAN)make mypy$(RESET)             Verificación de tipos estáticos"
	@echo ""
	@echo "$(BOLD)$(GREEN)⚙️  CELERY$(RESET)"
	@echo "  $(CYAN)make celery-status$(RESET)    Ver workers activos y colas"
	@echo "  $(CYAN)make celery-purge$(RESET)     ⚠️  Vaciar todas las colas de tareas"
	@echo "  $(CYAN)make celery-inspect$(RESET)   Ver tareas registradas en el worker"
	@echo "  $(CYAN)make flower$(RESET)           Abrir Flower (monitor web de Celery)"
	@echo ""
	@echo "$(BOLD)$(GREEN)🧹 MANTENIMIENTO$(RESET)"
	@echo "  $(CYAN)make collectstatic$(RESET)    Recolectar archivos estáticos"
	@echo "  $(CYAN)make clean$(RESET)            Borrar archivos temporales Python (__pycache__, .pyc)"
	@echo "  $(CYAN)make reset$(RESET)            💣 NUCLEAR: borrar contenedores + volúmenes + imágenes"
	@echo "  $(CYAN)make env-check$(RESET)        Verificar que todas las variables de entorno estén definidas"
	@echo ""

# ==============================================================================
# SECCIÓN 1 — ENTORNO
# ==============================================================================

.PHONY: dev
dev: env-check
	@echo "$(GREEN)🚀 Levantando MD Marketing & Diseño...$(RESET)"
	@echo "$(GRAY)   Django API   → http://localhost:8000$(RESET)"
	@echo "$(GRAY)   React App    → http://localhost:5173$(RESET)"
	@echo "$(GRAY)   Django Admin → http://localhost:8000/admin/$(RESET)"
	@echo "$(GRAY)   Health Check → http://localhost:8000/api/v1/health/$(RESET)"
	@echo ""
	$(DC) up --remove-orphans

.PHONY: dev-d
dev-d: env-check
	@echo "$(GREEN)🚀 Levantando en modo background...$(RESET)"
	$(DC) up -d --remove-orphans
	@echo "$(GREEN)✅ Servicios corriendo en background$(RESET)"
	@echo "$(GRAY)   Ver logs: make logs$(RESET)"

.PHONY: build
build:
	@echo "$(YELLOW)🔨 Reconstruyendo imágenes Docker...$(RESET)"
	$(DC) build --no-cache
	@echo "$(GREEN)✅ Build completo$(RESET)"

.PHONY: build-web
build-web:
	@echo "$(YELLOW)🔨 Reconstruyendo solo el Backend...$(RESET)"
	$(DC) build --no-cache $(WEB)

.PHONY: stop
stop:
	@echo "$(YELLOW)⏹  Deteniendo servicios...$(RESET)"
	$(DC) stop
	@echo "$(GREEN)✅ Servicios detenidos. Los datos están preservados.$(RESET)"

.PHONY: restart
restart:
	@echo "$(YELLOW)🔄 Reiniciando servicios...$(RESET)"
	$(DC) restart
	@echo "$(GREEN)✅ Reinicio completo$(RESET)"

.PHONY: restart-web
restart-web:
	@echo "$(YELLOW)🔄 Reiniciando solo Django...$(RESET)"
	$(DC) restart $(WEB)

.PHONY: status
status:
	@echo "$(CYAN)$(BOLD)Estado de contenedores:$(RESET)"
	$(DC) ps
	@echo ""
	@echo "$(CYAN)$(BOLD)Uso de recursos:$(RESET)"
	@docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" \
		md_web md_db md_redis md_celery md_celery_beat md_frontend 2>/dev/null || true


# ==============================================================================
# SECCIÓN 2 — BASE DE DATOS
# ==============================================================================

.PHONY: migrate
migrate:
	@echo "$(GREEN)🔄 Aplicando migraciones...$(RESET)"
	$(DC) exec $(WEB) python manage.py migrate --noinput
	@echo "$(GREEN)✅ Migraciones aplicadas$(RESET)"

.PHONY: migrations
migrations:
	@echo "$(GREEN)📝 Generando migraciones...$(RESET)"
	$(DC) exec $(WEB) python manage.py makemigrations
	@echo "$(GREEN)✅ Migraciones generadas$(RESET)"

.PHONY: migrations-check
migrations-check:
	@echo "$(CYAN)🔍 Verificando migraciones pendientes...$(RESET)"
	$(DC) exec $(WEB) python manage.py makemigrations --check --dry-run
	$(DC) exec $(WEB) python manage.py migrate --check
	@echo "$(GREEN)✅ Sin migraciones pendientes$(RESET)"

.PHONY: showmigrations
showmigrations:
	$(DC) exec $(WEB) python manage.py showmigrations

.PHONY: superuser
superuser:
	@echo "$(CYAN)👤 Creando superusuario...$(RESET)"
	$(DC) exec -it $(WEB) python manage.py createsuperuser
	@echo "$(GREEN)✅ Superusuario creado$(RESET)"

.PHONY: seed
seed:
	@echo "$(GREEN)🌱 Cargando datos iniciales...$(RESET)"
	$(DC) exec $(WEB) python manage.py loaddata fixtures/categorias_financieras.json
	$(DC) exec $(WEB) python manage.py loaddata fixtures/catalogo_base.json
	@echo "$(GREEN)✅ Datos iniciales cargados$(RESET)"

.PHONY: db-shell
db-shell:
	@echo "$(CYAN)🐘 Abriendo consola PostgreSQL...$(RESET)"
	$(DC) exec $(DB) psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

.PHONY: db-backup
db-backup:
	@mkdir -p backups
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S) && \
	FILENAME="backups/md_backup_$$TIMESTAMP.sql" && \
	echo "$(CYAN)💾 Generando backup: $$FILENAME$(RESET)" && \
	$(DC) exec $(DB) pg_dump -U $${POSTGRES_USER} $${POSTGRES_DB} > $$FILENAME && \
	echo "$(GREEN)✅ Backup guardado: $$FILENAME$(RESET)" && \
	ls -lh $$FILENAME

.PHONY: db-restore
db-restore:
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)❌ Error: especifica el archivo con FILE=backups/archivo.sql$(RESET)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)⚠️  Restaurando desde $(FILE)...$(RESET)"
	@read -p "¿Confirmas? Esto borrará todos los datos actuales. [s/N] " confirm && \
	[ "$$confirm" = "s" ] || [ "$$confirm" = "S" ] || exit 1
	$(DC) exec -T $(DB) psql -U $${POSTGRES_USER} -d $${POSTGRES_DB} < $(FILE)
	@echo "$(GREEN)✅ Restauración completa$(RESET)"

.PHONY: flush
flush:
	@echo "$(RED)⚠️  ADVERTENCIA: Esto borrará TODOS los datos de la base de datos.$(RESET)"
	@read -p "¿Confirmas? [s/N] " confirm && \
	[ "$$confirm" = "s" ] || [ "$$confirm" = "S" ] || exit 1
	$(DC) exec $(WEB) python manage.py flush --no-input
	@echo "$(YELLOW)🗑️  Datos borrados. Estructura de tablas intacta.$(RESET)"


# ==============================================================================
# SECCIÓN 3 — CONSOLAS
# ==============================================================================

.PHONY: shell
shell:
	@echo "$(CYAN)🐚 Abriendo Django shell...$(RESET)"
	$(DC) exec -it $(WEB) python manage.py shell_plus 2>/dev/null || \
	$(DC) exec -it $(WEB) python manage.py shell

.PHONY: bash
bash:
	@echo "$(CYAN)🐚 Bash en el contenedor web...$(RESET)"
	$(DC) exec -it $(WEB) bash

.PHONY: bash-celery
bash-celery:
	$(DC) exec -it $(CELERY) bash

.PHONY: redis-cli
redis-cli:
	@echo "$(CYAN)🔴 Abriendo Redis CLI...$(RESET)"
	$(DC) exec $(REDIS) redis-cli


# ==============================================================================
# SECCIÓN 4 — LOGS
# ==============================================================================

.PHONY: logs
logs:
	$(DC) logs -f --tail=50

.PHONY: logs-web
logs-web:
	@echo "$(CYAN)📋 Logs de Django (Ctrl+C para salir)$(RESET)"
	$(DC) logs -f --tail=100 $(WEB)

.PHONY: logs-celery
logs-celery:
	@echo "$(CYAN)📋 Logs de Celery worker + beat (Ctrl+C para salir)$(RESET)"
	$(DC) logs -f --tail=100 celery celery_beat

.PHONY: logs-db
logs-db:
	$(DC) logs -f --tail=50 $(DB)

.PHONY: logs-frontend
logs-frontend:
	$(DC) logs -f --tail=100 frontend


# ==============================================================================
# SECCIÓN 5 — TESTING Y CALIDAD DE CÓDIGO
# ==============================================================================

.PHONY: test
test:
	@echo "$(CYAN)🧪 Ejecutando tests con pytest...$(RESET)"
	$(DC) exec $(WEB) pytest tests/ -v --tb=short
	@echo "$(GREEN)✅ Tests completados$(RESET)"

.PHONY: test-cov
test-cov:
	@echo "$(CYAN)🧪 Tests con cobertura de código...$(RESET)"
	$(DC) exec $(WEB) pytest tests/ \
		--cov=apps \
		--cov-report=html:/app/htmlcov \
		--cov-report=term-missing \
		--cov-fail-under=70 \
		-v
	@echo "$(GREEN)✅ Reporte de cobertura: Backend/htmlcov/index.html$(RESET)"

.PHONY: test-fast
test-fast:
	@echo "$(CYAN)🧪 Tests rápidos (sin cobertura)...$(RESET)"
	$(DC) exec $(WEB) pytest tests/ -x --tb=short -q

.PHONY: test-app
## Uso: make test-app APP=crm
test-app:
	@if [ -z "$(APP)" ]; then echo "$(RED)Uso: make test-app APP=crm$(RESET)"; exit 1; fi
	$(DC) exec $(WEB) pytest tests/test_$(APP).py -v --tb=long

.PHONY: lint
lint:
	@echo "$(CYAN)🔍 Verificando estilo de código...$(RESET)"
	$(DC) exec $(WEB) flake8 apps/ tasks/ --max-line-length=100 --exclude=migrations
	$(DC) exec $(WEB) isort --check-only --diff apps/ tasks/
	@echo "$(GREEN)✅ Código cumple estándares$(RESET)"

.PHONY: format
format:
	@echo "$(YELLOW)✨ Formateando código...$(RESET)"
	$(DC) exec $(WEB) black apps/ tasks/ tests/ --line-length=100 --exclude=migrations
	$(DC) exec $(WEB) isort apps/ tasks/ tests/
	@echo "$(GREEN)✅ Código formateado$(RESET)"

.PHONY: mypy
mypy:
	@echo "$(CYAN)🔬 Verificación de tipos...$(RESET)"
	$(DC) exec $(WEB) mypy apps/ --ignore-missing-imports --exclude=migrations


# ==============================================================================
# SECCIÓN 6 — CELERY
# ==============================================================================

.PHONY: celery-status
celery-status:
	@echo "$(CYAN)⚙️  Estado de workers Celery:$(RESET)"
	$(DC) exec $(CELERY) celery -A config inspect active
	@echo ""
	@echo "$(CYAN)⚙️  Colas activas:$(RESET)"
	$(DC) exec $(CELERY) celery -A config inspect active_queues

.PHONY: celery-purge
celery-purge:
	@echo "$(RED)⚠️  Esto vaciará TODAS las tareas pendientes en la cola.$(RESET)"
	@read -p "¿Confirmas? [s/N] " confirm && \
	[ "$$confirm" = "s" ] || [ "$$confirm" = "S" ] || exit 1
	$(DC) exec $(CELERY) celery -A config purge -f
	@echo "$(YELLOW)🗑️  Colas vaciadas$(RESET)"

.PHONY: celery-inspect
celery-inspect:
	@echo "$(CYAN)⚙️  Tareas registradas en el worker:$(RESET)"
	$(DC) exec $(CELERY) celery -A config inspect registered

.PHONY: celery-ping
celery-ping:
	$(DC) exec $(CELERY) celery -A config inspect ping

.PHONY: flower
flower:
	@echo "$(CYAN)🌸 Iniciando Flower en http://localhost:5555$(RESET)"
	$(DC) exec -d $(CELERY) celery -A config flower --port=5555 --basic_auth=admin:md2024
	@echo "$(GREEN)✅ Flower corriendo: http://localhost:5555$(RESET)"


# ==============================================================================
# SECCIÓN 7 — MANTENIMIENTO
# ==============================================================================

.PHONY: collectstatic
collectstatic:
	@echo "$(CYAN)📦 Recolectando archivos estáticos...$(RESET)"
	$(DC) exec $(WEB) python manage.py collectstatic --noinput --clear
	@echo "$(GREEN)✅ Estáticos actualizados$(RESET)"

.PHONY: clean
clean:
	@echo "$(YELLOW)🧹 Limpiando archivos temporales Python...$(RESET)"
	find Backend/ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	find Backend/ -name "*.pyc" -delete 2>/dev/null; true
	find Backend/ -name "*.pyo" -delete 2>/dev/null; true
	find Backend/ -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null; true
	find Backend/ -name "htmlcov" -exec rm -rf {} + 2>/dev/null; true
	find Backend/ -name ".coverage" -delete 2>/dev/null; true
	@echo "$(GREEN)✅ Limpieza completa$(RESET)"

.PHONY: reset
reset:
	@echo ""
	@echo "$(RED)$(BOLD)╔══════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(RED)$(BOLD)║   💣  OPERACIÓN NUCLEAR — BORRADO TOTAL              ║$(RESET)"
	@echo "$(RED)$(BOLD)║                                                      ║$(RESET)"
	@echo "$(RED)$(BOLD)║   Se eliminarán:                                     ║$(RESET)"
	@echo "$(RED)$(BOLD)║   • Todos los contenedores                           ║$(RESET)"
	@echo "$(RED)$(BOLD)║   • Todos los volúmenes (incluye datos de la DB)     ║$(RESET)"
	@echo "$(RED)$(BOLD)║   • Imágenes Docker del proyecto                     ║$(RESET)"
	@echo "$(RED)$(BOLD)║                                                      ║$(RESET)"
	@echo "$(RED)$(BOLD)║   ⚠️  Esta operación es IRREVERSIBLE                 ║$(RESET)"
	@echo "$(RED)$(BOLD)╚══════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@read -p "Escribe 'RESET' para confirmar: " confirm && \
	[ "$$confirm" = "RESET" ] || (echo "$(GRAY)Operación cancelada$(RESET)" && exit 1)
	$(DC) down -v --remove-orphans --rmi local
	$(MAKE) clean
	@echo ""
	@echo "$(GREEN)✅ Reset completo. Ejecuta 'make build && make dev' para comenzar de nuevo.$(RESET)"

.PHONY: env-check
env-check:
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "$(RED)❌ Archivo .env no encontrado en la raíz del proyecto.$(RESET)"; \
		echo "$(YELLOW)   Copia Backend/.env.example a .env y completa los valores:$(RESET)"; \
		echo "$(GRAY)   cp Backend/.env.example .env$(RESET)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ Archivo .env encontrado$(RESET)"

.PHONY: env-show
env-show:
	@echo "$(CYAN)Variables de entorno cargadas:$(RESET)"
	@grep -v "^#" $(ENV_FILE) | grep -v "^$$" | sort


# ==============================================================================
# SECCIÓN 8 — ATAJOS DE DESARROLLO RÁPIDO
# ==============================================================================

# Flujo completo desde cero (primera vez)
.PHONY: setup
setup: env-check build dev-d
	@sleep 15
	@echo "$(CYAN)🔄 Esperando que los servicios estén listos...$(RESET)"
	$(DC) exec $(WEB) python manage.py migrate --noinput
	$(DC) exec $(WEB) python manage.py collectstatic --noinput
	@echo ""
	@echo "$(GREEN)$(BOLD)════════════════════════════════════════════════════$(RESET)"
	@echo "$(GREEN)$(BOLD)  ✅ MD Marketing & Diseño listo para desarrollar  $(RESET)"
	@echo "$(GREEN)$(BOLD)════════════════════════════════════════════════════$(RESET)"
	@echo ""
	@echo "  $(CYAN)Django API:$(RESET)   http://localhost:8000"
	@echo "  $(CYAN)React App:$(RESET)    http://localhost:5173"
	@echo "  $(CYAN)Admin:$(RESET)        http://localhost:8000/admin/"
	@echo "  $(CYAN)Health:$(RESET)       http://localhost:8000/api/v1/health/"
	@echo ""
	@echo "  $(YELLOW)Próximo paso: make superuser$(RESET)"
	@echo ""

# Ver URLs disponibles de la API
.PHONY: urls
urls:
	$(DC) exec $(WEB) python manage.py show_urls 2>/dev/null || \
	$(DC) exec $(WEB) python manage.py shell -c \
		"from django.urls import get_resolver; \
		[print(p) for p in get_resolver().url_patterns]"

# Abrir el Django Admin en el navegador (macOS/Linux)
.PHONY: admin
admin:
	@echo "$(CYAN)🌐 Abriendo Django Admin...$(RESET)"
	@open http://localhost:8000/admin/ 2>/dev/null || \
	 xdg-open http://localhost:8000/admin/ 2>/dev/null || \
	 echo "$(GRAY)   Navega a: http://localhost:8000/admin/$(RESET)"

# Abrir la aplicación React en el navegador
.PHONY: open
open:
	@open http://localhost:5173 2>/dev/null || \
	 xdg-open http://localhost:5173 2>/dev/null || \
	 echo "$(GRAY)   Navega a: http://localhost:5173$(RESET)"