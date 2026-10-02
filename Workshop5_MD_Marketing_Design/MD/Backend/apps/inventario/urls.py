# ==============================================================================
# MD Marketing & Diseño — apps/inventario/urls.py
# ==============================================================================

from rest_framework.routers import DefaultRouter
from .views import MateriaPrimaViewSet, ConsumoMateriaPrimaViewSet

app_name = "inventario"

router = DefaultRouter()
router.register(r"materias-primas", MateriaPrimaViewSet,        basename="materiaprima")
router.register(r"consumos",        ConsumoMateriaPrimaViewSet, basename="consumo")

urlpatterns = router.urls


# ==============================================================================
# MD Marketing & Diseño — apps/auth_urls.py
# PEGAR EN: Backend/apps/auth_urls.py
# ==============================================================================

# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView,
# )
#
# urlpatterns = [
#     path("token/",           TokenObtainPairView.as_view(),  name="token_obtain_pair"),
#     path("token/refresh/",   TokenRefreshView.as_view(),     name="token_refresh"),
#     path("token/blacklist/", TokenBlacklistView.as_view(),   name="token_blacklist"),
# ]