from api.admin import custom_admin_site
from django.urls import path, include

urlpatterns = [
    path('admin/', custom_admin_site.urls),

    path('', include('api.urls.html_urls')),

    path('api/', include('api.urls.api_urls')),
]