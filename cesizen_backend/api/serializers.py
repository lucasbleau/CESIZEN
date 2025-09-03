from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from api.models import (
    ExerciceRespiration,
    HistoriqueExercice,
    Information,
    Utilisateur,  # si ton modèle custom s'appelle Utilisateur
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'first_name', 'last_name']

    def validate_username(self, value):
        user = self.context['request'].user
        if Utilisateur.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value

    def validate_email(self, value):
        user = self.context['request'].user
        if Utilisateur.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ("id", "email", "username", "role", "is_superuser")
        read_only_fields = ("id", "role", "is_superuser")

class ExerciceRespirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciceRespiration
        fields = (
            "id",
            "nom",
            "duree_inspiration",
            "duree_apnee",
            "duree_expiration",
            "description",
        )

    def validate(self, attrs):
        erreurs = {}
        for champ in ("duree_inspiration", "duree_apnee", "duree_expiration"):
            if attrs.get(champ, 0) < 0:
                erreurs[champ] = "La durée ne peut pas être négative."
        if erreurs:
            raise serializers.ValidationError(erreurs)
        return attrs

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ("id", "titre", "contenu", "date_creation", "date_modification")
        read_only_fields = ("id", "date_creation", "date_modification")

class HistoriqueExerciceSerializer(serializers.ModelSerializer):
    exercice = ExerciceRespirationSerializer(read_only=True)
    exercice_id = serializers.PrimaryKeyRelatedField(
        queryset=ExerciceRespiration.objects.all(),
        source="exercice",
        write_only=True
    )

    class Meta:
        model = HistoriqueExercice
        fields = (
            "id",
            "exercice",
            "exercice_id",
            "date_effectue",
            "duree_totale",
        )
        read_only_fields = ("id", "date_effectue")

    def create(self, validated_data):
        validated_data["utilisateur"] = self.context["request"].user
        return super().create(validated_data)

class MessageResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


# === Mapping pour les tests: ConnexionSerializer / InscriptionSerializer ===

class ConnexionSerializer(serializers.Serializer):
    """
    Serializer d'authentification simple (mapping demandé par les tests).
    Attend email + password (ou username si ton USERNAME_FIELD diffère).
    Retourne l'utilisateur authentifié dans validated_data['user'].
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )
        if not user:
            raise serializers.ValidationError({"detail": "Identifiants invalides"})
        attrs["user"] = user
        return attrs


class InscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer d'inscription (mapping demandé par les tests).
    Crée un utilisateur via create_user pour hasher le mot de passe.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Utilisateur
        # Ajuste si les tests attendent d'autres champs (ex: first_name, last_name)
        fields = ("email", "username", "password")

    def validate_email(self, value):
        if Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email déjà utilisé.")
        return value

    def validate_username(self, value):
        if Utilisateur.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username déjà utilisé.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Utilisateur.objects.create_user(password=password, **validated_data)
        return user

# Optionnel: pour que from api.serializers import * expose aussi ces noms
__all__ = [
    "UserSerializer",
    "ProfilSerializer",
    "UtilisateurSerializer",
    "ExerciceRespirationSerializer",
    "InformationSerializer",
    "HistoriqueExerciceSerializer",
    "MessageResponseSerializer",
    "ErrorResponseSerializer",
    "EmailTokenObtainPairSerializer",
    "ConnexionSerializer",
    "InscriptionSerializer",
]
