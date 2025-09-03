from django.contrib import admin
from django.urls import path, include
from api.views.cookie_views import (
    InscriptionView, ConnexionView, UpgradeAdminView, RefreshCookieView
)
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls.api_urls")),
    path("", include("api.urls.html_urls")),
    path("api/inscription/", InscriptionView.as_view(), name="api_inscription"),
    path("api/connexion/", ConnexionView.as_view(), name="api_connexion"),
    path("api/upgrade-admin/<int:user_id>/", UpgradeAdminView.as_view(), name="api_upgrade_admin"),
    path("api/token/refresh-cookie/", RefreshCookieView.as_view(), name="refresh-cookie"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]