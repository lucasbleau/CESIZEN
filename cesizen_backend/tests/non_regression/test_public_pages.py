import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_homepage_is_public(client):
    r = client.get(reverse("accueil"))
    assert r.status_code == 200
    assert b"CESIZEN" in r.content
