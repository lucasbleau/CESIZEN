from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from api.models import ExerciceRespiration, HistoriqueExercice
from api.serializers import (
    HistoriqueExerciceSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)


@extend_schema(
    tags=["Historique"],
    responses={200: HistoriqueExerciceSerializer(many=True)},
    methods=["GET"]
)
@extend_schema(
    request=HistoriqueExerciceSerializer,
    responses={
        201: MessageResponseSerializer,
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer
    },
    methods=["POST"]
)
class HistoriqueExerciceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        historiques = HistoriqueExercice.objects.filter(utilisateur=request.user)
        serializer = HistoriqueExerciceSerializer(historiques, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HistoriqueExerciceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Données invalides."}, status=400)

        exercice = ExerciceRespiration.objects.get(id=serializer.validated_data["exercice_id"])

        HistoriqueExercice.objects.create(
            utilisateur=request.user,
            exercice=exercice,
            duree_totale=serializer.validated_data["duree_totale"]
        )

        return Response({"message": "Historique enregistré"}, status=201)
