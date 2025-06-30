import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_detail_exercice_inexistant():
    client = APIClient()
    r = client.get(reverse("api_exercice_detail", kwargs={"pk": 999}))
    assert r.status_code == 404
