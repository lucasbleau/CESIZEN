import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Utilisateur

@pytest.mark.django_db
def test_inscription_et_connexion():
    client = APIClient()

    resp_signup = client.post(reverse("api_inscription"), {
        "email": "test@example.com",
        "username": "tester",
        "password1": "MyPwd123!",
        "password2": "MyPwd123!"
    }, format="json")
    assert resp_signup.status_code == 201

    resp_login = client.post(reverse("api_connexion"), {
        "email": "test@example.com",
        "password": "MyPwd123!"
    }, format="json")
    assert resp_login.status_code == 200
    assert "access" in resp_login.data or "message" in resp_login.data
