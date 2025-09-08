from django.urls import path
from api.views.utilisateur_views import ProfileMeView
from api.views.info_views import AccueilView
from api.views.exercice_views import ListeExercicesView, DetailExerciceView
from api.views.historique_views import HistoriqueExerciceView
from api.views.cookie_views import CookieLoginView, CookieLogoutView, CookieRefreshView, InscriptionView

urlpatterns = [
    path("profil/", ProfileMeView.as_view(), name="api_profil"),
    path("accueil/", AccueilView.as_view(), name="api_accueil"),
    path("exercices/", ListeExercicesView.as_view(), name="api_exercices"),
    path("exercices/<int:pk>/", DetailExerciceView.as_view(), name="api_exercice_detail"),
    path("historique/", HistoriqueExerciceView.as_view(), name="api_historique"),
    # Auth cookies
    path("token/cookie/", CookieLoginView.as_view(), name="cookie_login"),
    path("token/cookie/refresh/", CookieRefreshView.as_view(), name="token_cookie_refresh"),
    path("token/cookie/logout/", CookieLogoutView.as_view(), name="token_cookie_logout"),
    path("deconnexion/", CookieLogoutView.as_view(), name="api_deconnexion"),  # alias GET
    path("inscription/", InscriptionView.as_view(), name="api_inscription"),
]