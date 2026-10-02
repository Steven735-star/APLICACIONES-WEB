# ==============================================================================
# MD Marketing & Diseño — apps/produccion/urls.py
# ==============================================================================

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, OrdenItemViewSet, KanbanView

app_name = "produccion"

router = DefaultRouter()
router.register(r"ordenes", OrdenViewSet,     basename="orden")
router.register(r"items",   OrdenItemViewSet, basename="ordenitem")

urlpatterns = router.urls + [
    path("kanban/", KanbanView.as_view(), name="kanban"),
]