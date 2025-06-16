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
            for field in ['username', 'email', 'first_name', 'last_name']:
                if field in serializer.validated_data:
                    setattr(user, field, serializer.validated_data[field])
            user.save()
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
