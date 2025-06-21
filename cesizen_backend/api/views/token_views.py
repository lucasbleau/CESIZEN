from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings

class RefreshAccessTokenView(APIView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token manquant."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            response = Response({"message": "Access token régénéré."})
            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
                path="/"
            )
            return response

        except (TokenError, InvalidToken) as e:
            return Response({"error": str(e)}, status=401)
