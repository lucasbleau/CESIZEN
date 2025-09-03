from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework_simplejwt.tokens import AccessToken

from api.models import HistoriqueExercice
from api.serializers import HistoriqueExerciceSerializer, ErrorResponseSerializer, MessageResponseSerializer

User = get_user_model()


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
        # Session déjà authentifiée ?
        if not request.user or not request.user.is_authenticated:
            token_str = request.COOKIES.get("access_token")
            if token_str:
                try:
                    at = AccessToken(token_str)
                    user_id = at.get("user_id")
                    request.user = User.objects.get(pk=user_id)
                except Exception:
                    return Response({"detail": "Authentification requise."}, status=401)
            else:
                return Response({"detail": "Authentification requise."}, status=401)

        ser = HistoriqueExerciceSerializer(data=request.data, context={"request": request})
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        try:
            obj = ser.save()
        except serializers.ValidationError as e:
            return Response(e.detail, status=400)
        return Response({"id": obj.id}, status=201)
