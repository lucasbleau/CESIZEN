from rest_framework.views import APIView
from rest_framework.response import Response

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Déconnecté"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response