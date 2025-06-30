import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_openapi_schema_accessible():
    client = APIClient()
    resp = client.get(reverse("schema"))
    assert resp.status_code == 200
    assert resp.data.get("openapi")
