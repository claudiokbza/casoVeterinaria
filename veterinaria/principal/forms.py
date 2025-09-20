from django import forms
from .models import Dueno, FichaMascota, Atencion

class FichaMascotaForm(forms.ModelForm):
    class Meta:
        model = FichaMascota
        fields = ['nombre', 'num_chip', 'sexo', 'fecha_nacimiento', 'raza', 'dueño', 'asistente']

class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = ['diagnostico', 'tratamiento', 'observaciones', 'ficha_mascota', 'veterinario']