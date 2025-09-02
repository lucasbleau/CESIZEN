from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Lit le token JWT d'accès dans le cookie 'access_token'.
    """
    def authenticate(self, request):
        raw = request.COOKIES.get("access_token")
        if not raw:
            return None
        token = self.get_validated_token(raw)
        return (self.get_user(token), token)
