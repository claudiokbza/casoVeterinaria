from django.contrib import admin
from .models import Profesional, Asistente, Veterinario

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('run', 'nombre', 'apellido', 'fono')
    search_fields = ('run', 'nombre', 'apellido')

@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ('idasistente', 'tipo_acceso')

@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('idveterinario', 'tipo_acceso')