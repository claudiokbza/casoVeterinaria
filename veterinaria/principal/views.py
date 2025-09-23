from django.shortcuts import render, redirect, get_object_or_404
from .forms import FichaMascotaForm, AtencionForm, DuenoForm
from django.http import HttpResponseForbidden 
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import Perfil 
from .models import FichaMascota, Atencion, Asistente, Veterinario, Dueno
from datetime import date



#FICHAS MASCOTAS


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
        form = DuenoForm()
        context = {'form': form, 'title': 'Crear Dueño'}
        return render(request, 'principal/form_dueno.html', context)

def buscar_dueno(request):
    if request.method == 'POST':
        run_ingresado = request.POST.get('run', '').strip()

        # Validamos que el RUN no esté vacío
        if not run_ingresado:
            messages.error(request, 'Por favor, ingrese un RUN para buscar.')
            return redirect('buscar_dueno')

        # Buscamos al dueño por su RUN
        dueno = Dueno.objects.filter(run=run_ingresado).first()

        if dueno:
            # Si el dueño existe, lo redirigimos a crear la ficha de la mascota
            messages.success(request, f'Dueño encontrado. Ahora puede registrar a la mascota.')
            return redirect('crear_ficha_mascota', dueno_pk=dueno.pk)
        else:
            # Si el dueño NO existe, lo redirigimos al formulario de creación
            messages.info(request, f'Dueño con RUN {run_ingresado} no encontrado. Por favor, registre sus datos.')
            return redirect('crear_dueno')
            
    return render(request, 'principal/buscar_dueno.html')

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
    atenciones = Atencion.objects.filter(ficha_mascota=mascota).order_by('-fecha_atencion')
    return render(request, 'principal/detalle_mascota.html', {'mascota': mascota, 'atenciones': atenciones})



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
    mascota = get_object_or_404(FichaMascota, pk=mascota_pk)

    if request.method == 'POST':
        form = AtencionForm(request.POST)
        if form.is_valid():
            nueva_atencion = form.save(commit=False)
            nueva_atencion.ficha_mascota = mascota              # <- asigna la ficha
            nueva_atencion.fecha_atencion = date.today()        # <- si tu modelo NO tiene default
            veterinario = Veterinario.objects.first()           # <- provisional
            if veterinario:
                nueva_atencion.veterinario = veterinario
            nueva_atencion.save()
            return redirect('detalle_mascota', pk=mascota.pk)
    else:
        form = AtencionForm()                                   # <- sin initial inválido

    return render(
        request,
        'principal/form_atencion.html',
        {'form': form, 'title': 'Crear Atención', 'mascota': mascota}  # <- pasa mascota
    )


def modificar_atencion(request, pk):
    atencion = get_object_or_404(Atencion, pk=pk)
    if request.method == 'POST':
        form = AtencionForm(request.POST, instance=atencion)
        if form.is_valid():
            form.save()
            return redirect('detalle_mascota', pk=atencion.ficha_mascota.pk)
    else:
        form = AtencionForm(instance=atencion)
    context = {
        'form': form,
        'title': 'Modificar Atención',
        'mascota': atencion.ficha_mascota
    }
    return render(request, 'principal/form_atencion.html', context)

def eliminar_atencion(request, pk):
    atencion = get_object_or_404(Atencion, pk=pk)
    mascota_pk = atencion.ficha_mascota.pk
    if request.method == 'POST':
        atencion.delete()
        return redirect('detalle_mascota', pk=mascota_pk)
    return render(request, 'principal/confirmar_eliminar_atencion.html', {'atencion': atencion})

def home(request):
    return render(request, 'principal/home.html')
