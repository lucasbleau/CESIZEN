from django.contrib import admin
from django.urls import path
from api.views import accueil, connexion, deconnexion, inscription, liste_exercices, preferences, profil, profil_edit, upgrade_to_admin

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', accueil, name='accueil'),
    path('upgrade_admin/<int:user_id>/', upgrade_to_admin, name='upgrade_admin'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('inscription/', inscription, name='inscription'),
    path('exercices/', liste_exercices, name='liste_exercices'),
    path('profil/', profil, name='profil'),
    path('profil/edit/', profil_edit, name='profil_edit'),
    path('preferences/', preferences, name='preferences'),
]
