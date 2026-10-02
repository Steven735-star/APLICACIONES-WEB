# ==============================================================================
# MD Marketing & Diseño — apps/finanzas/urls.py
# ==============================================================================

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaFinancieraViewSet, TransaccionViewSet,
    ReporteUtilidadView, ReporteIVAView,
    ReporteTendenciaView, ReporteEgresosView,
    DashboardResumenView,
)

app_name = "finanzas"

router = DefaultRouter()
router.register(r"categorias",    CategoriaFinancieraViewSet, basename="categoria")
router.register(r"transacciones", TransaccionViewSet,         basename="transaccion")

urlpatterns = router.urls + [
    path("reportes/utilidad/",  ReporteUtilidadView.as_view(),  name="reporte-utilidad"),
    path("reportes/iva/",       ReporteIVAView.as_view(),       name="reporte-iva"),
    path("reportes/tendencia/", ReporteTendenciaView.as_view(), name="reporte-tendencia"),
    path("reportes/egresos/",   ReporteEgresosView.as_view(),   name="reporte-egresos"),
    path("dashboard/",          DashboardResumenView.as_view(), name="dashboard"),
]