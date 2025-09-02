from django.urls import path
from api.views.utilisateur_views import ProfileMeView
from api.views.info_views import AccueilView
from api.views.exercice_views import ListeExercicesView, DetailExerciceView
from api.views.historique_views import HistoriqueExerciceView
from api.views.cookie_views import CookieLoginView, CookieRefreshView, LogoutView, InscriptionView

urlpatterns = [
    path("profil/", ProfileMeView.as_view(), name="api_profil"),
    path("accueil/", AccueilView.as_view(), name="api_accueil"),
    path("exercices/", ListeExercicesView.as_view(), name="api_exercices"),
    path("exercices/<int:pk>/", DetailExerciceView.as_view(), name="api_exercice_detail"),
    path("historique/", HistoriqueExerciceView.as_view(), name="api_historique"),
    path("token/cookie/", CookieLoginView.as_view(), name="cookie_login"),
    path("token/cookie/refresh/", CookieRefreshView.as_view(), name="cookie_refresh"),
    path("deconnexion/", LogoutView.as_view(), name="api_deconnexion"),
    path("inscription/", InscriptionView.as_view(), name="api_inscription"),
]