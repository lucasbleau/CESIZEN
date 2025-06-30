import pytest
from django.db import IntegrityError
from api.models import Utilisateur

@pytest.mark.django_db
def test_utilisateur_email_unique_en_base():

    Utilisateur.objects.create_user(email="dup@y.com", username="u1", password="x")
    with pytest.raises(IntegrityError):
        Utilisateur.objects.create_user(email="dup@y.com", username="u2", password="x")
