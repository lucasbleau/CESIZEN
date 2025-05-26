from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from api.models import Utilisateur, ExerciceRespiration, Information
from api.serializers import (
    ConnexionSerializer,
    InscriptionSerializer,
    InformationSerializer,
    ExerciceRespirationSerializer,
    ProfilSerializer,
    UtilisateurSerializer,
    UserSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)

@extend_schema(tags=['Accueil'])
class AccueilView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=InformationSerializer)
    def get(self, request):
        informations = Information.objects.all()
        serializer = InformationSerializer(informations, many=True)
        return Response(serializer.data)

@extend_schema(tags=['Profil'])
class ProfilView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProfilSerializer)
    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)

    @extend_schema(request=ProfilSerializer, responses=ProfilSerializer)
    def put(self, request):
        user = request.user
        serializer = ProfilSerializer(data=request.data)

        if serializer.is_valid():
            user.username = serializer.validated_data['username']
            user.email = serializer.validated_data['email']
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@extend_schema(tags=['Admin'])
class UpgradeToAdminView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=MessageResponseSerializer)
    def post(self, request, user_id):
        user = get_object_or_404(Utilisateur, id=user_id)
        user.role = "administrateur"
        user.save()
        return Response({"detail": "Rôle mis à jour en administrateur."})

@extend_schema(tags=['Connexion'],
    request=ConnexionSerializer,
    responses={
        200: MessageResponseSerializer,
        401: ErrorResponseSerializer
    })
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

@extend_schema(tags=['Inscription'],
    request=InscriptionSerializer,
    responses={
        201: MessageResponseSerializer,
        400: ErrorResponseSerializer
    })
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

        Utilisateur.objects.create_user(
            email=email,
            username=username,
            password=password1
        )

        return Response({"detail": "Inscription réussie."}, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Deconnexion'], responses=MessageResponseSerializer)
class DeconnexionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Déconnexion réussie."})

@extend_schema(tags=['Exercices'], responses=ExerciceRespirationSerializer)
class ListeExercicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exercices = ExerciceRespiration.objects.all()
        serializer = ExerciceRespirationSerializer(exercices, many=True)
        return Response(serializer.data)