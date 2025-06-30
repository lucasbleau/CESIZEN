import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Utilisateur


@pytest.mark.django_db
def test_profil_get_non_authentifie():
    client = APIClient()
    r = client.get(reverse("api_profil"))
    assert r.status_code == 401


# @pytest.mark.django_db
# def test_profil_email_deja_pris():
#     Utilisateur.objects.create_user(email="dup@y.com", username="dup", password="pwd")
#     user2 = Utilisateur.objects.create_user(email="b@x.com", username="b", password="pwd")
#     client = APIClient()
#     client.force_authenticate(user2)
#     r = client.put(reverse("api_profil"), {
#         "email": "dup@y.com",
#         "username": "b"
#     }, format="json")
#     assert r.status_code == 400
#     assert "already exists" in str(r.data["email"][0])
