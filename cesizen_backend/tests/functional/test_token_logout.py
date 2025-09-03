import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Utilisateur


# @pytest.mark.django_db
# def test_refresh_cookie_endpoint():
#     u = Utilisateur.objects.create_user(email="r@x.com", username="r", password="p")
#     refresh = RefreshToken.for_user(u)
#     client = APIClient()
#     client.cookies["refresh_token"] = str(refresh)

#     r = client.post(reverse("refresh-cookie"))
#     assert r.status_code == 200
#     assert "access_token" in r.cookies


@pytest.mark.django_db
def test_deconnexion_supprime_cookies():
    u = Utilisateur.objects.create_user(email="d@x.com", username="d", password="p")
    client = APIClient()
    client.force_authenticate(u)

    client.cookies["access_token"] = "abc"
    client.cookies["refresh_token"] = "def"

    r = client.post(reverse("api_deconnexion"))
    assert r.status_code == 200
    assert r.cookies["access_token"].value == ""
    assert r.cookies["refresh_token"].value == ""
