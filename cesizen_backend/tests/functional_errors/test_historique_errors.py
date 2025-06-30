import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Utilisateur, ExerciceRespiration


@pytest.mark.django_db
def test_historique_post_sans_auth():
    client = APIClient()
    r = client.post(reverse("api_historique"), {
        "exercice_id": 1,
        "duree_totale": 10
    }, format="json")
    assert r.status_code == 401


@pytest.mark.django_db
def test_historique_post_exercice_invalide():
    user = Utilisateur.objects.create_user(email="a@a.com", username="a", password="pwd")
    client = APIClient()
    client.force_authenticate(user)
    r = client.post(reverse("api_historique"), {
        "exercice_id": 123456,  # inexistant
        "duree_totale": 12
    }, format="json")
    assert r.status_code == 400
    assert "exercice" in str(r.data).lower()
