from urllib import response
from django.shortcuts import redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from api.serializers import ConnexionSerializer, InscriptionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = InscriptionSerializer(data=request.data)
        if not ser.is_valid():
            # ser.errors est déjà {"error": "..."} si custom, sinon formater
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        # Vérifs DB (duplication) ici (functional tests marqués django_db)
        if User.objects.filter(email=ser.validated_data["email"]).exists():
            return Response({"error": "Email déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=ser.validated_data["username"]).exists():
            return Response({"error": "Username déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)
        user = ser.save()
        return Response({"id": user.id, "email": user.email}, status=status.HTTP_201_CREATED)


class ConnexionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = ConnexionSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            request=request,
            email=ser.validated_data["email"],
            password=ser.validated_data["password"]
        )
        if not user:
            return Response({"error": "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class UpgradeAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if not request.user.is_superuser:
            return Response({"error": "Accès refusé"}, status=status.HTTP_403_FORBIDDEN)
        cible = get_object_or_404(User, pk=user_id)
        cible.is_superuser = True
        if hasattr(cible, "role"):
            try:
                cible.role = "administrateur"
            except Exception:
                pass
        cible.save()
        return Response({"detail": "Utilisateur promu"}, status=status.HTTP_200_OK)


class RefreshCookieView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_str = request.COOKIES.get("refresh_token")
        if not token_str:
            return Response({"error": "Aucun refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(token_str)
            access = refresh.access_token
            return Response({"access": str(access)})
        except Exception:
            return Response({"error": "Refresh invalide"}, status=status.HTTP_400_BAD_REQUEST)