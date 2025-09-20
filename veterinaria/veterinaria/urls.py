from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # La URL raíz ('') ahora apunta directamente a las URLs de tu aplicación principal
    path('', include('principal.urls')),
    path('admin/', admin.site.urls),
]