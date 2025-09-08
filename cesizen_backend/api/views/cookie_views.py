from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import ConnexionSerializer, InscriptionSerializer

try:
    from rest_framework_simplejwt.tokens import RefreshToken
    from rest_framework_simplejwt.exceptions import TokenError
except Exception:
    RefreshToken = None

    class TokenError(Exception):
        ...


CK = dict(httponly=True, secure=not settings.DEBUG, samesite="Lax", path="/")
User = get_user_model()


class CookieLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = getattr(request, "data", {}) or {}
        email = (
            data.get("email")
            or data.get("username")
            or request.POST.get("email")
            or request.POST.get("username")
        )
        password = data.get("password") or request.POST.get("password")
        next_url = request.GET.get("next") or data.get("next") or "/"
        if not email or not password:
            return Response({"error": "Email et mot de passe requis."}, status=400)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Identifiants invalides."}, status=401)

        login(request, user)
        if not RefreshToken:
            return Response({"error": "SimpleJWT indisponible."}, status=500)

        r = RefreshToken.for_user(user)
        a = r.access_token

        wants_html = "text/html" in request.headers.get("Accept", "")
        if wants_html and isinstance(next_url, str) and next_url.startswith("/"):
            resp = redirect(next_url)
        else:
            resp = Response({"detail": "Connexion réussie.", "redirect_to": next_url})

        resp.set_cookie(
            "access_token",
            str(a),
            max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
            **CK,
        )
        resp.set_cookie(
            "refresh_token",
            str(r),
            max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
            **CK,
        )
        return resp


@method_decorator(csrf_exempt, name="dispatch")
class CookieRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token_str = request.COOKIES.get("refresh_token")
        if not token_str:
            return Response({"error": "Refresh token manquant."}, status=401)
        try:
            if not RefreshToken:
                return Response({"error": "SimpleJWT indisponible."}, status=500)
            r = RefreshToken(token_str)
            a = r.access_token
            resp = Response({"detail": "Access régénéré."})
            resp.set_cookie(
                "access_token",
                str(a),
                max_age=int(
                    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                ),
                **CK,
            )
            return resp
        except TokenError:
            return Response({"error": "Refresh invalide."}, status=401)


@method_decorator(csrf_exempt, name="dispatch")
class CookieLogoutView(APIView):
    permission_classes = [AllowAny]

    def _clear(self, resp: Response) -> Response:
        # Effacement robuste: delete + set vide max_age=0 avec mêmes attributs
        for name in ("access_token", "refresh_token"):
            resp.delete_cookie(name, path="/")
            resp.set_cookie(name, "", max_age=0, **CK)
        return resp

    def _do_logout(self, request):
        token_str = request.COOKIES.get("refresh_token")
        if token_str and RefreshToken:
            try:
                RefreshToken(token_str).blacklist()  # ignore si blacklist non activée
            except Exception:
                pass
        logout(request)

    def post(self, request):
        self._do_logout(request)
        resp = Response({"message": "Déconnecté"}, status=200)
        return self._clear(resp)

    def get(self, request):
        # Autorise les liens <a> GET et gère la redirection HTML
        self._do_logout(request)
        next_url = request.GET.get("next") or "/"
        wants_html = "text/html" in request.headers.get("Accept", "")
        resp = redirect(next_url) if wants_html else Response({"message": "Déconnecté"}, status=200)
        return self._clear(resp)


class InscriptionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = InscriptionSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=ser.validated_data["email"]).exists():
            return Response({"error": "Email déjà utilisé."}, status=400)
        if User.objects.filter(username=ser.validated_data["username"]).exists():
            return Response({"error": "Username déjà utilisé."}, status=400)
        user = ser.save()
        return Response({"id": user.id, "email": user.email}, status=201)


class ConnexionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = ConnexionSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = authenticate(
            request=request,
            email=ser.validated_data["email"],
            password=ser.validated_data["password"],
        )
        if not user:
            return Response({"error": "Identifiants invalides"}, status=400)
        if not RefreshToken:
            return Response({"error": "SimpleJWT indisponible."}, status=500)
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class UpgradeAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if not request.user.is_superuser:
            return Response({"error": "Accès refusé"}, status=403)
        cible = get_object_or_404(User, pk=user_id)
        cible.is_superuser = True
        if hasattr(cible, "role"):
            try:
                cible.role = "administrateur"
            except Exception:
                pass
        cible.save()
        return Response({"detail": "Utilisateur promu"}, status=200)


class RefreshCookieView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_str = request.COOKIES.get("refresh_token")
        if not token_str:
            return Response({"error": "Aucun refresh token"}, status=400)
        try:
            if not RefreshToken:
                return Response({"error": "SimpleJWT indisponible."}, status=500)
            refresh = RefreshToken(token_str)
            access = refresh.access_token
            return Response({"access": str(access)})
        except Exception:
            return Response({"error": "Refresh invalide"}, status=400)


# --- Aliases rétro-compat pour anciens noms importés ailleurs ---
LoginView = CookieLoginView
LogoutView = CookieLogoutView
CookieRefreshTokenView = CookieRefreshView
RefreshCookieTokenView = RefreshCookieView
TokenRefreshCookieView = RefreshCookieView