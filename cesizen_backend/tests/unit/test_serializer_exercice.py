from api.serializers import ExerciceRespirationSerializer
from api.models import ExerciceRespiration


def test_exercice_serializer_fields():
    exo = ExerciceRespiration(
        nom="4-7-8",
        duree_inspiration=4,
        duree_apnee=7,
        duree_expiration=8,
        description="Relaxation"
    )
    serializer = ExerciceRespirationSerializer(exo)
    data = serializer.data

    assert data["nom"] == "4-7-8"
    assert data["duree_inspiration"] == 4
    assert data["duree_apnee"] == 7
    assert data["duree_expiration"] == 8
