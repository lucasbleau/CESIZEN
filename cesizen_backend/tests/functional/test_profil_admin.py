import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Utilisateur


@pytest.fixture
def user():
    return Utilisateur.objects.create_user(
        email="u@x.com", username="u", password="pwd"
    )


@pytest.fixture
def admin():
    a = Utilisateur.objects.create_user(
        email="adm@x.com", username="adm", password="pwd", role="administrateur"
    )
    a.is_staff = True
    a.save()
    return a


@pytest.mark.django_db
def test_profil_get_put(user):
    client = APIClient()
    client.force_authenticate(user)

    r = client.get(reverse("api_profil"))
    assert r.status_code == 200
    assert r.data["email"] == user.email

    new_name = "newu"
    r2 = client.put(reverse("api_profil"), {"username": new_name}, format="json")
    assert r2.status_code == 200
    assert r2.data["username"] == new_name


# @pytest.mark.django_db
# def test_upgrade_admin(admin):
#     """Un admin promeut un autre utilisateur."""
#     target = Utilisateur.objects.create_user(email="t@x.com", username="t", password="pwd")

#     client = APIClient()
#     client.force_authenticate(admin)

#     url = reverse("api_upgrade_admin", kwargs={"user_id": target.id})
#     r = client.post(url)
#     assert r.status_code == 200
#     target.refresh_from_db()
#     assert target.role == "administrateur"
