from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from api.models import Information
from api.serializers import InformationSerializer


@extend_schema(tags=['Accueil'], responses=InformationSerializer(many=True))
class AccueilView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=InformationSerializer)
    def get(self, request):
        infos = Information.objects.all().order_by("-date_modification")
        return Response(InformationSerializer(infos, many=True).data)
