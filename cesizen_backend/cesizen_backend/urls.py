from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('api.urls.html_urls')),

    path('api/', include('api.urls.api_urls')),
]