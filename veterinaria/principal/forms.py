from django import forms
from .models import Dueno, FichaMascota, Atencion

class FichaMascotaForm(forms.ModelForm):

    class Meta:
        model = FichaMascota
        exclude = ['dueño'] # 'asistente' fue removido para que aparezca en el form
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bucle para añadir clases a los campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
        

# forms.py
class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = ['fecha_atencion', 'veterinario', 'diagnostico', 'tratamiento', 'observaciones']
        widgets = {
            'fecha_atencion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'diagnostico': forms.Textarea(attrs={'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['run', 'nombres', 'apellidos', 'email', 'fono_contacto1', 'fono_contacto2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Este bucle añade la clase 'form-control' a todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'