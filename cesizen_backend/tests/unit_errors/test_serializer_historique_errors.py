import pytest
from rest_framework.test import APIRequestFactory
from api.serializers import HistoriqueExerciceSerializer
from api.models import Utilisateur
from rest_framework.exceptions import ValidationError

factory = APIRequestFactory()

@pytest.mark.django_db
def test_historique_serializer_exercice_inexistant():

    user = Utilisateur.objects.create_user(email="u@x.com", username="u", password="pwd")
    req = factory.post("/")
    req.user = user

    ser = HistoriqueExerciceSerializer(
        data={"exercice_id": 9999, "duree_totale": 10},
        context={"request": req},
    )
    assert ser.is_valid()

    with pytest.raises(ValidationError) as exc:
        ser.save()
    assert "exercice_id" in exc.value.detail
