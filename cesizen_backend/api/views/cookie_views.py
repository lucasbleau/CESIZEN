from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers import ConnexionSerializer, InscriptionSerializer, MessageResponseSerializer, ErrorResponseSerializer
from api.models import Utilisateur
from django.conf import settings
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

@extend_schema(
    tags=["Authentification"],
    request=ConnexionSerializer,
    responses={
        200: MessageResponseSerializer,
        401: ErrorResponseSerializer
    }
)
class CookieLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConnexionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Données invalides."}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        remember = request.data.get("remember", False)

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({"message": "Connexion réussie."}, status=status.HTTP_200_OK)

        is_secure = not settings.DEBUG  # Utilise HTTPS si en production

        access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()) if remember else None
        refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()) if remember else None

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=is_secure,
            samesite="Lax",
            max_age=access_max_age,
            path="/"
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=is_secure,
            samesite="Lax",
            max_age=refresh_max_age,
            path="/"
        )

        return response



@extend_schema(
    tags=["Inscription"],
    request=InscriptionSerializer,
    responses={
        201: MessageResponseSerializer,
        400: ErrorResponseSerializer,
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
        remember = data.get("remember", False)

        if password1 != password2:
            return Response({"error": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)

        if Utilisateur.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        if Utilisateur.objects.filter(username=username).exists():
            return Response({"error": "Ce nom d'utilisateur est déjà pris."}, status=status.HTTP_400_BAD_REQUEST)

        utilisateur = Utilisateur.objects.create_user(email=email, username=username, password=password1)

        user = authenticate(request, username=email, password=password1)
        if not user:
            return Response({"error": "Erreur lors de l'authentification."}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({"detail": "Inscription réussie."}, status=status.HTTP_201_CREATED)

        is_secure = not settings.DEBUG

        access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()) if remember else None
        refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()) if remember else None

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=is_secure,
            samesite="Lax",
            max_age=access_max_age,
            path="/"
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=is_secure,
            samesite="Lax",
            max_age=refresh_max_age,
            path="/"
        )
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Déconnexion réussie."})

        response.delete_cookie(
            "access_token",
            path="/",
            domain=None,
            samesite="Lax"
        )
        response.delete_cookie(
            "refresh_token",
            path="/",
            domain=None,
            samesite="Lax"
        )

        return response