import pytest
from django.urls import reverse
from api.models import ExerciceRespiration

@pytest.mark.django_db
def test_liste_exercices_200(api_client):
    ExerciceRespiration.objects.create(nom="55", duree_inspiration=5,
                                       duree_apnee=0, duree_expiration=5,
                                       description="")
    r = api_client.get(reverse("api_exercices"))
    assert r.status_code == 200
    assert len(r.json()) == 1

@pytest.mark.django_db
def test_detail_exercice_anonyme(api_client):
    exo = ExerciceRespiration.objects.create(nom="748",
        duree_inspiration=7, duree_apnee=4, duree_expiration=8, description="")
    r = api_client.get(reverse("api_exercice_detail", kwargs={"pk": exo.id}))
    body = r.json()
    assert body["duree_inspiration"] == 7
