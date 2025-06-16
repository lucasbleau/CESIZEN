from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
from api.serializers import ConnexionSerializer, InscriptionSerializer, MessageResponseSerializer, ErrorResponseSerializer
from api.models import Utilisateur


@extend_schema(
    tags=['Connexion'],
    request=ConnexionSerializer,
    responses={
        200: OpenApiResponse(response=MessageResponseSerializer, description="Connexion OK"),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Échec de l'authentification")
    }
)
class ConnexionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": f"Bienvenue {user.username} !"})
        return Response({"error": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    tags=['Inscription'],
    request=InscriptionSerializer,
    responses={
        201: MessageResponseSerializer,
        400: ErrorResponseSerializer
    }
)
class InscriptionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            return Response({"error": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)

        if Utilisateur.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        if Utilisateur.objects.filter(username=username).exists():
            return Response({"error": "Ce nom d'utilisateur est déjà pris."}, status=status.HTTP_400_BAD_REQUEST)

        utilisateur = Utilisateur.objects.create_user(
            email=email,
            username=username,
            password=password1
        )

        user = authenticate(request, username=email, password=password1)
        if user:
            login(request, user)

        return Response({"detail": "Inscription réussie."}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Deconnexion'],
    responses=MessageResponseSerializer
)
class DeconnexionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Déconnexion réussie."})
