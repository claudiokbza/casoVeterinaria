from django.urls import path
from . import views

urlpatterns = [
    # La URL vacía ahora apunta a la vista lista_mascotas
    path('', views.lista_mascotas, name='lista_mascotas'),

    # El resto de tus URLs ya no necesitan el prefijo 'principal/'
    path('crear/', views.crear_ficha_mascota, name='crear_ficha_mascota'),
    path('<int:pk>/', views.detalle_mascota, name='detalle_mascota'),
    path('<int:pk>/modificar/', views.modificar_ficha_mascota, name='modificar_ficha_mascota'),
    path('<int:pk>/eliminar/', views.eliminar_ficha_mascota, name='eliminar_ficha_mascota'),
    path('atencion/crear/<int:mascota_pk>/', views.crear_atencion, name='crear_atencion'),
    path('atencion/<int:pk>/modificar/', views.modificar_atencion, name='modificar_atencion'),
    path('atencion/<int:pk>/eliminar/', views.eliminar_atencion, name='eliminar_atencion'),
]
