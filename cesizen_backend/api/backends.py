from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Utilisateur.objects.get(email=username)
            if user.check_password(password):
                return user
        except Utilisateur.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            return None
