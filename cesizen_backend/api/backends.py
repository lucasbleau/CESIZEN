from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        ident = email or username or kwargs.get("login")
        if not ident or not password:
            return None
        try:
            user = User.objects.get(email=ident)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=ident)
            except User.DoesNotExist:
                return None
        return user if user.check_password(password) else None

    def get_user(self, user_id):
        try: return User.objects.get(pk=user_id)
        except User.DoesNotExist: return None
