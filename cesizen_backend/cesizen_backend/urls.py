"""
URL configuration for cesizen_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
