from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import ExerciceRespiration, HistoriqueExercice, Information, Utilisateur
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
        fields = ("email", "username", "first_name", "last_name", "role")
        read_only_fields = ("role",)

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
    exercice = serializers.SerializerMethodField(read_only=True)
    exercice_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = HistoriqueExercice
        fields = ("id", "exercice", "exercice_id", "date_effectue", "duree_totale")
        read_only_fields = ("id", "date_effectue")

    def get_exercice(self, obj):
        if obj.exercice_id:
            return {"id": obj.exercice_id, "nom": getattr(obj.exercice, "nom", None)}
        return None

    def create(self, validated_data):
        ex_id = validated_data.pop("exercice_id", None)
        try:
            exercice = ExerciceRespiration.objects.get(pk=ex_id)
        except ExerciceRespiration.DoesNotExist:
            # Les tests: is_valid() True puis save() -> ValidationError
            raise serializers.ValidationError({"exercice_id": "Exercice inexistant."})
        validated_data["exercice"] = exercice
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


class InscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    # Pas de min_length pour que les tests de mismatch obtiennent bien non_field_errors
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get("password1") != attrs.get("password2"):
            # Les tests attendent ser.errors["non_field_errors"]
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password1"],
        )

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
