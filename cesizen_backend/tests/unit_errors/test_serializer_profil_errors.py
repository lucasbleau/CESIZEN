import pytest
from rest_framework.test import APIRequestFactory
from api.serializers import ProfilSerializer
from api.models import Utilisateur

factory = APIRequestFactory()

@pytest.mark.django_db
def test_profil_serializer_duplicate_email_and_username():
    Utilisateur.objects.create_user(username="dup", email="dup@y.com", password="x")
    current = Utilisateur.objects.create_user(username="cur", email="cur@y.com", password="x")

    req = factory.put("/")
    req.user = current

    ser = ProfilSerializer(
        instance=current,
        data={"email": "dup@y.com", "username": "dup"},
        context={"request": req},
    )

    assert not ser.is_valid()
    assert ser.errors["email"][0].code == "unique"
    assert ser.errors["username"][0].code == "unique"
