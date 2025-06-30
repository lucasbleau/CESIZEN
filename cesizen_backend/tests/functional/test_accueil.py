import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Information, Utilisateur


@pytest.mark.django_db
def test_accueil_retourne_liste_public():
    """L’endpoint est public : on récupère les infos sans auth."""
    Information.objects.bulk_create([
        Information(titre="T1", contenu="...", createur=Utilisateur.objects.create_user(
            email="a@a.com", username="a", password="x")),
        Information(titre="T2", contenu="...", createur=Utilisateur.objects.first())
    ])

    client = APIClient()
    resp = client.get(reverse("api_accueil"))
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    assert {"titre", "contenu"} <= resp.json()[0].keys()