from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from api.models import Utilisateur, ExerciceRespiration, HistoriqueExercice, Information

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
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'last_login', 'is_superuser']

class ExerciceRespirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciceRespiration
        fields = '__all__'

class HistoriqueExerciceSerializer(serializers.ModelSerializer):
    exercice_id = serializers.IntegerField(write_only=True)
    exercice_nom = serializers.CharField(source="exercice.nom", read_only=True)

    class Meta:
        model = HistoriqueExercice
        fields = ["exercice_id", "exercice_nom", "date_effectue", "duree_totale"]

    def create(self, validated_data):
        exercice_id = validated_data.pop("exercice_id")
        exercice = ExerciceRespiration.objects.get(id=exercice_id)
        utilisateur = self.context["request"].user
        return HistoriqueExercice.objects.create(
            utilisateur=utilisateur,
            exercice=exercice,
            **validated_data
        )

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class ConnexionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class InscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

class MessageResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
