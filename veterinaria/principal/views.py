from django.shortcuts import render, redirect, get_object_or_404
from .forms import FichaMascotaForm, AtencionForm, DuenoForm
from django.http import HttpResponseForbidden 
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import Perfil 
from .models import FichaMascota, Atencion, Asistente, Veterinario, Dueno


#FICHAS MASCOTAS

# En principal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Dueno, FichaMascota, Asistente
from .forms import DuenoForm, FichaMascotaForm
from django.core.exceptions import ObjectDoesNotExist

# En principal/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Dueno, FichaMascota, Asistente
from .forms import DuenoForm, FichaMascotaForm
from django.core.exceptions import ObjectDoesNotExist

def crear_dueno(request):
    if request.method == 'POST':
        # Primero, intenta encontrar un dueño existente usando el RUN del formulario
        run_ingresado = request.POST.get('run')
        dueno_existente = Dueno.objects.filter(run=run_ingresado).first()

        if dueno_existente:
            # Si el dueño ya existe, lo usamos y redirigimos
            messages.info(request, f'Dueño con RUN {run_ingresado} ya existe. Se usará este perfil.')
            return redirect('crear_ficha_mascota', dueno_pk=dueno_existente.pk)
        
        else:
            # Si el dueño no existe, validamos el formulario y lo creamos
            form = DuenoForm(request.POST)
            if form.is_valid():
                dueno_nuevo = form.save()
                messages.success(request, 'Datos del dueño guardados correctamente.')
                return redirect('crear_ficha_mascota', dueno_pk=dueno_nuevo.pk)
            else:
                # Si el formulario no es válido (por otros errores que no sean el RUN duplicado),
                # se muestran los errores y se renderiza el formulario de nuevo.
                context = {'form': form, 'title': 'Crear Dueño'}
                return render(request, 'principal/form_dueno.html', context)
    
    else:
        # Petición GET, muestra el formulario vacío
        form = DuenoForm()
        context = {'form': form, 'title': 'Crear Dueño'}
        return render(request, 'principal/form_dueno.html', context)

def crear_ficha_mascota(request, dueno_pk):
    dueno = get_object_or_404(Dueno, pk=dueno_pk)

    if request.method == 'POST':
        form = FichaMascotaForm(request.POST)
        if form.is_valid():
            ficha_mascota = form.save(commit=False)
            ficha_mascota.dueño = dueno
            
            asistente = Asistente.objects.first()
            if asistente:
                ficha_mascota.asistente = asistente
                ficha_mascota.save()
                messages.success(request, 'Ficha de la mascota guardada correctamente.')
                return redirect('lista_mascotas')
            else:
                messages.error(request, 'No se puede crear una ficha sin un asistente.')
                return redirect('crear_dueno')
    else:
        form = FichaMascotaForm()

    context = {'form': form, 'title': 'Crear Ficha de Mascota'}
    return render(request, 'principal/form_ficha_mascota.html', context)

def lista_mascotas(request):
    mascotas = FichaMascota.objects.all()
    return render(request, 'principal/lista_mascotas.html', {'mascotas': mascotas})

def detalle_mascota(request, pk):
    mascota = get_object_or_404(FichaMascota, pk=pk)
    return render(request, 'principal/detalle_mascota.html', {'mascota': mascota})


def modificar_ficha_mascota(request, pk):
    mascota = get_object_or_404(FichaMascota, pk=pk)
    if request.method == 'POST':
        form = FichaMascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('detalle_mascota', pk=mascota.pk)
    else:
        form = FichaMascotaForm(instance=mascota)
    return render(request, 'principal/form_ficha_mascota.html', {'form': form, 'title': 'Modificar Ficha'})

def eliminar_ficha_mascota(request, pk):
    mascota = get_object_or_404(FichaMascota, pk=pk)
    if request.method == 'POST':
        mascota.delete()
        return redirect('lista_mascotas')
    return render(request, 'principal/confirmar_eliminar_mascota.html', {'mascota': mascota})

#ATENCIONES

def crear_atencion(request, mascota_pk):
    mascota = FichaMascota.objects.get(pk=mascota_pk)
    if request.method == 'POST':
        form = AtencionForm(request.POST)
        if form.is_valid():
            nueva_atencion = form.save(commit=False)
            veterinario = Veterinario.objects.first() # Obtiene el primer veterinario
            if veterinario:
                nueva_atencion.veterinario = veterinario
                nueva_atencion.save()
                return redirect('detalle_mascota', pk=mascota.pk)
            else:
                return redirect('detalle_mascota', pk=mascota.pk)
    else:
        form = AtencionForm(initial={'mascota': mascota})
    return render(request, 'principal/form_atencion.html', {'form': form, 'title': 'Crear Atención'})

def detalle_mascota(request, pk):
    mascota = get_object_or_404(FichaMascota, pk=pk)
    atenciones = Atencion.objects.filter(ficha_mascota=mascota).order_by('-fecha_atencion')
    return render(request, 'principal/detalle_mascota.html', {'mascota': mascota, 'atenciones': atenciones})

def modificar_atencion(request, pk):
    atencion = get_object_or_404(Atencion, pk=pk)
    if request.method == 'POST':
        form = AtencionForm(request.POST, instance=atencion)
        if form.is_valid():
            form.save()
            return redirect('detalle_mascota', pk=atencion.ficha_mascota.pk)
    else:
        form = AtencionForm(instance=atencion)
    return render(request, 'principal/form_atencion.html', {'form': form, 'title': 'Modificar Atención'}) 

def eliminar_atencion(request, pk):
    atencion = get_object_or_404(Atencion, pk=pk)
    mascota_pk = atencion.ficha_mascota.pk
    if request.method == 'POST':
        atencion.delete()
        return redirect('detalle_mascota', pk=mascota_pk)
    return render(request, 'principal/confirmar_eliminar_atencion.html', {'atencion': atencion})
