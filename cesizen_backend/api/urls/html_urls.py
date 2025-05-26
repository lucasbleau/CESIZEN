from django.urls import path
from api.views.html_views import accueil, connexion, inscription, deconnexion, preferences, profil, profil_edit

urlpatterns = [
    path('', accueil, name='accueil'),
    path('connexion/', connexion, name='connexion'),
    path('inscription/', inscription, name='inscription'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('preferences/', preferences, name='preferences'),
    path('profil/', profil, name='profil'),
    path('profil/edit/', profil_edit, name='profil_edit'),
]