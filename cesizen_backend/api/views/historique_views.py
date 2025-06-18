from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from api.models import ExerciceRespiration, HistoriqueExercice
from api.serializers import HistoriqueExerciceSerializer


@extend_schema(tags=["Historique"], responses=HistoriqueExerciceSerializer(many=True))
class HistoriqueExerciceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        historiques = HistoriqueExercice.objects.filter(utilisateur=request.user).order_by('-date_effectue')
        serializer = HistoriqueExerciceSerializer(historiques, many=True)
        return Response(serializer.data)

    def post(self, request):
        exercice_id = request.data.get("exercice_id")
        duree_totale = request.data.get("duree_totale")

        if not exercice_id or not duree_totale:
            return Response({"error": "Données manquantes"}, status=400)

        try:
            exercice = ExerciceRespiration.objects.get(id=exercice_id)
        except ExerciceRespiration.DoesNotExist:
            return Response({"error": "Exercice introuvable"}, status=404)

        HistoriqueExercice.objects.create(
            utilisateur=request.user,
            exercice=exercice,
            duree_totale=duree_totale,
        )

        return Response({"message": "Historique enregistré"}, status=201)
