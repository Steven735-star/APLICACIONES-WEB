# ==============================================================================
# MD Marketing & Diseño — apps/auth_urls.py
# Endpoints de autenticación JWT
# ==============================================================================

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    # POST { "username": "...", "password": "..." }
    # → { "access": "...", "refresh": "..." }
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    # POST { "refresh": "..." }
    # → { "access": "...", "refresh": "..." }
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # POST { "refresh": "..." }
    # → 200 OK (invalida el refresh token — logout)
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]