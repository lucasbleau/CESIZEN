import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Utilisateur


# @pytest.mark.django_db
# def test_refresh_cookie_sans_refresh():
#     client = APIClient()
#     r = client.post(reverse("refresh-cookie"))
#     assert r.status_code == 401


@pytest.mark.django_db
def test_upgrade_admin_par_non_superuser():
    normal = Utilisateur.objects.create_user(email="n@n.com", username="n", password="pwd")
    cible  = Utilisateur.objects.create_user(email="c@c.com", username="c", password="pwd")

    client = APIClient()
    client.force_authenticate(normal)

    r = client.post(reverse("api_upgrade_admin", kwargs={"user_id": cible.id}))
    assert r.status_code == 403
