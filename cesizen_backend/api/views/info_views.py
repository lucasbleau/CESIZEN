from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from api.models import Information
from api.serializers import InformationSerializer


@extend_schema(tags=['Accueil'])
class AccueilView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=InformationSerializer)
    def get(self, request):
        informations = Information.objects.all()
        serializer = InformationSerializer(informations, many=True)
        return Response(serializer.data)
