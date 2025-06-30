import pytest
from api.models import Utilisateur, ExerciceRespiration, HistoriqueExercice
from django.test import override_settings

@pytest.mark.django_db
@override_settings(PASSWORD_HASHERS=[
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
])
def test_password_hashed_with_pbkdf2():
    u = Utilisateur.objects.create_user(
        email="x@y.com", username="x", password="secret"
    )
    assert u.password.startswith("pbkdf2_")

@pytest.mark.django_db
def test_duree_totale_property():
    exo = ExerciceRespiration.objects.create(
        nom="test", duree_inspiration=4, duree_apnee=2, duree_expiration=4, description=""
    )
    histo = HistoriqueExercice(exercice=exo, utilisateur=None, duree_totale=10)
    assert histo.duree_totale == 10
