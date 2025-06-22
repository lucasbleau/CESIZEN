from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
from django.shortcuts import get_object_or_404
from api.models import Utilisateur
from api.serializers import ProfilSerializer, MessageResponseSerializer
from api.serializers import UtilisateurSerializer

@extend_schema(tags=['Profil'], responses=UtilisateurSerializer)
class ProfilView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UtilisateurSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UtilisateurSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Admin'])
class UpgradeToAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(responses=MessageResponseSerializer)
    def post(self, request, user_id):
        user = get_object_or_404(Utilisateur, id=user_id)
        user.role = "administrateur"
        user.save()
        return Response({"detail": "Rôle mis à jour en administrateur."})
