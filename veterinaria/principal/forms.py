from django import forms
from .models import Dueno, FichaMascota, Atencion

class FichaMascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de nacimiento"
    )
    class Meta:
        model = FichaMascota
        fields = ['nombre', 'num_chip', 'sexo', 'fecha_nacimiento', 'raza', 'dueño', 'asistente']
        exclude = ['dueño']
        

class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = ['diagnostico', 'tratamiento', 'observaciones', 'ficha_mascota', 'veterinario']

class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['run', 'nombres', 'apellidos', 'email', 'fono_contacto1', 'fono_contacto2']