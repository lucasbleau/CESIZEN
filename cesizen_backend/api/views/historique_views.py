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
        ser = HistoriqueExerciceSerializer(historiques, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = HistoriqueExerciceSerializer(data=request.data, context={"request": request})
        
        if ser.is_valid():
            historique = ser.save()
            return Response(
                HistoriqueExerciceSerializer(historique).data,
                status=201
            )
        return Response(ser.errors, status=400)
