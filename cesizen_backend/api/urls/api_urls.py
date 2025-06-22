from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    InscriptionView, LogoutView,
    AccueilView, ListeExercicesView,
    ProfilView, UpgradeToAdminView,
    HistoriqueExerciceView, CookieLoginView,
    RefreshAccessTokenView
)


urlpatterns = [
    path('accueil/', AccueilView.as_view(), name='api_accueil'),

    path('connexion/', CookieLoginView.as_view(), name='api_connexion'),
    path('inscription/', InscriptionView.as_view(), name='api_inscription'),
    path('deconnexion/', LogoutView.as_view(), name='api_deconnexion'),

    path('exercices/', ListeExercicesView.as_view(), name='api_exercices'),
    
    path('historique/', HistoriqueExerciceView.as_view(), name='api_historique'),

    path('profil/', ProfilView.as_view(), name='api_profil'),
    path('upgrade_admin/<int:user_id>/', UpgradeToAdminView.as_view(), name='api_upgrade_admin'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('token/cookie/', CookieLoginView.as_view(), name='cookie_login'),
    path("token/refresh-cookie/", RefreshAccessTokenView.as_view(), name="refresh-cookie"),
]