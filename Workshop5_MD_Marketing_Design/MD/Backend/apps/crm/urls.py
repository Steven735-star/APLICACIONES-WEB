# ==============================================================================
# MD Marketing & Diseño — apps/crm/urls.py
# ==============================================================================

from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, CatalogoItemViewSet

app_name = "crm"

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet,      basename="cliente")
router.register(r"catalogo", CatalogoItemViewSet, basename="catalogo")

urlpatterns = router.urls