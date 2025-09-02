from urllib import response
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()
CK = dict(httponly=True, secure=not settings.DEBUG, samesite="Lax", path="/")

class CookieLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = getattr(request, "data", {})
        email = data.get("email") or data.get("username") or request.POST.get("email") or request.POST.get("username")
        password = data.get("password") or request.POST.get("password")
        next_url = request.GET.get("next") or data.get("next") or "/"
        if not email or not password:
            return Response({"error": "Email et mot de passe requis."}, status=400)
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Identifiants invalides."}, status=401)
        login(request, user)
        r = RefreshToken.for_user(user)
        a = r.access_token
        # Redirection serveur si requête HTML classique
        wants_html = "text/html" in request.headers.get("Accept","")
        if wants_html and next_url.startswith("/"):
            resp = redirect(next_url)
        else:
            resp = Response({"detail": "Connexion réussie.", "redirect_to": next_url})
        resp.set_cookie("access_token", str(a), max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()), **CK)
        resp.set_cookie("refresh_token", str(r), max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()), **CK)
        return resp

class CookieRefreshView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token_str = request.COOKIES.get("refresh_token")
        if not token_str:
            return Response({"error": "Refresh token manquant."}, status=401)
        try:
            r = RefreshToken(token_str)
            a = r.access_token
            resp = Response({"detail": "Access régénéré."})
            resp.set_cookie("access_token", str(a), max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()), **CK)
            return resp
        except TokenError:
            return Response({"error": "Refresh invalide."}, status=401)

class CookieLogoutView(APIView):
    def post(self, request):
        logout(request)
        resp = Response({"detail": "Déconnexion."})
        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/")
        return resp

class InscriptionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = getattr(request, "data", {})
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        if not all([email, username, password]):
            return Response({"error": "Champs manquants."}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email déjà utilisé."}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Nom déjà utilisé."}, status=400)
        u = User(email=email, username=username)
        u.set_password(password)
        u.save()
        return Response({"detail": "Compte créé."}, status=201)

class LogoutView(CookieLogoutView):
    pass