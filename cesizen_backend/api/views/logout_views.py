from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from api.serializers import MessageResponseSerializer

@extend_schema(tags=["Authentification"], responses=MessageResponseSerializer)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Déconnecté"})
        response.delete_cookie("access_token", samesite="Lax", path="/")
        response.delete_cookie("refresh_token", samesite="Lax", path="/")   
        return response