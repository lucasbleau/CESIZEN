from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views.api_views import (
    AccueilView, ConnexionView, InscriptionView, DeconnexionView,
    ListeExercicesView, ProfilView, UpgradeToAdminView
)

urlpatterns = [
    path('accueil/', AccueilView.as_view(), name='api_accueil'),
    path('connexion/', ConnexionView.as_view(), name='api_connexion'),
    path('inscription/', InscriptionView.as_view(), name='api_inscription'),
    path('deconnexion/', DeconnexionView.as_view(), name='api_deconnexion'),
    path('exercices/', ListeExercicesView.as_view(), name='api_exercices'),
    path('profil/', ProfilView.as_view(), name='api_profil'),
    path('upgrade_admin/<int:user_id>/', UpgradeToAdminView.as_view(), name='api_upgrade_admin'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]