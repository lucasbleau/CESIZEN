from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Utilisateur, ExerciceRespiration, HistoriqueExercice, Information

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfilSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'role']

class ExerciceRespirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciceRespiration
        fields = '__all__'

class HistoriqueExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueExercice
        fields = '__all__'

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
