import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Utilisateur

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    u = Utilisateur.objects.create_user(
        email="user@test.com",
        username="user",
        password="Pwd123!!"
    )
    u.is_active = True
    u.save()
    return u

@pytest.fixture
def auth_client(api_client, user):
    api_client.post(
        reverse("api_connexion"),
        {"email": user.email, "password": "Pwd123!!"},
        format="json"
    )
    return api_client
