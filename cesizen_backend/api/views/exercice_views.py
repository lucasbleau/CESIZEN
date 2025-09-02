from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from api.models import ExerciceRespiration
from api.serializers import ExerciceRespirationSerializer


@extend_schema(tags=['Exercices'], responses=ExerciceRespirationSerializer(many=True))
class ListeExercicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exos = ExerciceRespiration.objects.all().order_by("id")
        return Response(ExerciceRespirationSerializer(exos, many=True).data)

class DetailExerciceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        exo = get_object_or_404(ExerciceRespiration, pk=pk)
        return Response(ExerciceRespirationSerializer(exo).data)