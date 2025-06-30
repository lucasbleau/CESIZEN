import pytest
from rest_framework.test import APIRequestFactory
from api.serializers import HistoriqueExerciceSerializer
from api.models import Utilisateur, ExerciceRespiration


@pytest.mark.django_db
def test_historique_serializer_create():
    user = Utilisateur.objects.create_user(username="u", email="u@u.com", password="u")
    exercice = ExerciceRespiration.objects.create(
        nom="5-5", duree_inspiration=5, duree_apnee=0, duree_expiration=5, description="desc"
    )

    data = {"exercice_id": exercice.id, "duree_totale": 10}
    factory = APIRequestFactory()
    request = factory.post("/")
    request.user = user

    serializer = HistoriqueExerciceSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors

    historique = serializer.save()
    assert historique.utilisateur == user
    assert historique.exercice == exercice
    assert historique.duree_totale == 10
