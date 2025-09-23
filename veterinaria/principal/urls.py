from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('mascotas/', views.lista_mascotas, name='lista_mascotas'),
    path('duenos/crear/', views.crear_dueno, name='crear_dueno'),
    path('duenos/buscar/', views.buscar_dueno, name='buscar_dueno'),
    path('fichas/crear/<int:dueno_pk>/', views.crear_ficha_mascota, name='crear_ficha_mascota'),
    path('<int:pk>/', views.detalle_mascota, name='detalle_mascota'),
    path('<int:pk>/modificar/', views.modificar_ficha_mascota, name='modificar_ficha_mascota'),
    path('<int:pk>/eliminar/', views.eliminar_ficha_mascota, name='eliminar_ficha_mascota'),
    path('atencion/crear/<int:mascota_pk>/', views.crear_atencion, name='crear_atencion'),
    path('atencion/<int:pk>/modificar/', views.modificar_atencion, name='modificar_atencion'),
    path('atencion/<int:pk>/eliminar/', views.eliminar_atencion, name='eliminar_atencion'),
]
