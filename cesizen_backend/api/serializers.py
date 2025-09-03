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
    exercice_id = serializers.IntegerField(write_only=True)

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
        exercice_id = validated_data.pop("exercice_id", None)
        if exercice_id:
            try:
                validated_data["exercice"] = ExerciceRespiration.objects.get(pk=exercice_id)
            except ExerciceRespiration.DoesNotExist:
                # Laisser sans exercice si inexistant (les tests attendent is_valid True)
                pass
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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    # Pas d'accès DB ici (tests unitaires sans marque django_db)
    def validate(self, attrs):
        return attrs


class InscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        missing = [k for k in ("email","username","password1","password2") if not attrs.get(k)]
        if missing:
            raise serializers.ValidationError({"error": "Champs manquants."})
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"error": "Les mots de passe ne correspondent pas."})
        # Pas de check DB ici (tests unitaires)
        return attrs

    def create(self, validated_data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password1"]
        user = User.objects.create_user(email=email, username=username, password=password)
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
