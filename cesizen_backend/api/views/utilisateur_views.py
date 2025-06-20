from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
from django.shortcuts import get_object_or_404
from api.models import Utilisateur
from api.serializers import ProfilSerializer, MessageResponseSerializer


@extend_schema(tags=['Profil'])
class ProfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": getattr(user, "role", None),
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
        })

    def put(self, request):
        user = request.user
        serializer = ProfilSerializer(user, data=request.data, partial=True, context={'request': request})
        
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
