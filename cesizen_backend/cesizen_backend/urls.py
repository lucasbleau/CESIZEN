from api.admin import custom_admin_site
from django.urls import path, include
from django.http import JsonResponse

def health(_r): return JsonResponse({"status":"ok"})

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('health/', health),
    path('', include('api.urls.html_urls')),
    path('api/', include('api.urls.api_urls')),
]