from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from api.models import ExerciceRespiration
from api.serializers import ExerciceRespirationSerializer


@extend_schema(tags=['Exercices'], responses=ExerciceRespirationSerializer)
class ListeExercicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exercices = ExerciceRespiration.objects.all()
        serializer = ExerciceRespirationSerializer(exercices, many=True)
        return Response(serializer.data)
