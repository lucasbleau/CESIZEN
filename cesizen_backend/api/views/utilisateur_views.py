from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from api.models import Utilisateur
from api.serializers import UtilisateurSerializer, MessageResponseSerializer

@extend_schema(tags=['Profil'], responses=UtilisateurSerializer)
class ProfileMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UtilisateurSerializer(request.user).data)

    def put(self, request):
        ser = UtilisateurSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    patch = put

@extend_schema(tags=['Admin'])
class UpgradeToAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(responses=MessageResponseSerializer)
    def post(self, request, user_id):
        user = get_object_or_404(Utilisateur, id=user_id)
        user.role = "administrateur"
        user.save()
        return Response({"detail": "Rôle mis à jour en administrateur."})
