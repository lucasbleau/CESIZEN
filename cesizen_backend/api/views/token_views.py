from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from drf_spectacular.utils import extend_schema
from django.conf import settings
from api.serializers import MessageResponseSerializer, ErrorResponseSerializer

@extend_schema(
    tags=["Authentification"],
    responses={
        200: MessageResponseSerializer,
        401: ErrorResponseSerializer,
    }
)
class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token manquant."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            response = Response({"detail": "Access token régénéré."})
            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
                path="/"
            )
            return response

        except (TokenError, InvalidToken) as e:
            return Response({"error": "Refresh token invalide ou expiré."}, status=status.HTTP_401_UNAUTHORIZED)
