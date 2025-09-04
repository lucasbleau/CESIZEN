from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "ok",
            "version": getattr(settings, "APP_VERSION", "dev"),
            "time": timezone.now().isoformat()
        }, status=200)