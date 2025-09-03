import pytest
from django.urls import reverse
from api.models import ExerciceRespiration, HistoriqueExercice

# @pytest.mark.django_db
# def test_historique_flow(auth_client, user):
#     exo = ExerciceRespiration.objects.create(nom="46", duree_inspiration=4,
#                                              duree_apnee=0, duree_expiration=6,
#                                              description="")
#     r = auth_client.post(reverse("api_historique"),
#                          {"exercice_id": exo.id, "duree_totale": 10},
#                          format="json")
#     assert r.status_code == 201
#     r = auth_client.get(reverse("api_historique"))
#     assert r.status_code == 200
#     assert len(r.json()) == 1
#     assert HistoriqueExercice.objects.filter(utilisateur=user).count() == 1
