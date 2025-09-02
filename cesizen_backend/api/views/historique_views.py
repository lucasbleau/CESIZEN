from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from api.models import HistoriqueExercice
from api.serializers import HistoriqueExerciceSerializer, ErrorResponseSerializer, MessageResponseSerializer


@extend_schema(
    tags=["Historique"],
    responses={200: HistoriqueExerciceSerializer(many=True)},
    methods=["GET"]
)
@extend_schema(
    request=HistoriqueExerciceSerializer,
    responses={201: HistoriqueExerciceSerializer, 400: ErrorResponseSerializer},
    methods=["POST"]
)
class HistoriqueExerciceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = HistoriqueExercice.objects.filter(utilisateur=request.user).select_related("exercice").order_by("-date_effectue")
        return Response(HistoriqueExerciceSerializer(qs, many=True).data)

    def post(self, request):
        ser = HistoriqueExerciceSerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            obj = ser.save()
            return Response(HistoriqueExerciceSerializer(obj).data, status=201)
        return Response(ser.errors, status=400)
