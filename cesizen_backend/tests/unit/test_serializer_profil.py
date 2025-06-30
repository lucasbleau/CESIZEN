import pytest
from api.serializers import ProfilSerializer
from api.models import Utilisateur
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
def test_profil_serializer_unique_email_and_username():
    Utilisateur.objects.create_user(username="test1", email="t1@x.com", password="x")
    existing_user = Utilisateur.objects.create_user(username="test2", email="t2@x.com", password="x")

    factory = APIRequestFactory()
    request = factory.get("/")
    request.user = existing_user

    serializer = ProfilSerializer(
        instance=existing_user,
        data={"email": "t1@x.com", "username": "test2"},
        context={"request": request}
    )

    assert not serializer.is_valid()
    assert "email" in serializer.errors
