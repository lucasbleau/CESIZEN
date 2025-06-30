import pytest
from api.serializers import ExerciceRespirationSerializer

def test_exercice_serializer_valeurs_negatives():

    ser = ExerciceRespirationSerializer(
        data={
            "nom": "KO",
            "duree_inspiration": -1,
            "duree_apnee": 0,
            "duree_expiration": 5,
            "description": "test"
        }
    )
    assert not ser.is_valid()
    assert "duree_inspiration" in ser.errors
