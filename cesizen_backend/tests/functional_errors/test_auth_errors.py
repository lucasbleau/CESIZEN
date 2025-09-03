import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Utilisateur


# @pytest.mark.django_db
# def test_inscription_mdp_non_correspondants():
#     client = APIClient()
#     resp = client.post(reverse("api_inscription"), {
#         "email": "x@y.com",
#         "username": "userx",
#         "password1": "abc123!",
#         "password2": "XXX123!",
#     }, format="json")
#     assert resp.status_code == 400
#     assert resp.data["error"].startswith("Les mots de passe")


@pytest.mark.django_db
def test_inscription_email_duplique():
    Utilisateur.objects.create_user(email="dup@y.com", username="dup", password="pwd")
    client = APIClient()
    resp = client.post(reverse("api_inscription"), {
        "email": "dup@y.com",
        "username": "newdup",
        "password1": "Pwd123!",
        "password2": "Pwd123!",
    }, format="json")
    assert resp.status_code == 400
    assert "déjà utilisé" in resp.data["error"]


# @pytest.mark.django_db
# def test_connexion_mauvais_password():
#     Utilisateur.objects.create_user(email="z@y.com", username="z", password="goodPwd1!")
#     client = APIClient()
#     r = client.post(reverse("api_connexion"), {
#         "email": "z@y.com",
#         "password": "badPwd!"
#     }, format="json")
#     assert r.status_code == 401
#     assert r.data["error"].startswith("Email ou mot de passe")
