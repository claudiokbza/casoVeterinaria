from django.shortcuts import render, redirect, get_object_or_404
from .forms import FichaMascotaForm, AtencionForm 
from django.http import HttpResponseForbidden 
from functools import wraps 
from .models import Perfil 
from .models import FichaMascota, Atencion, Asistente, Veterinario

def rol_requerido(rol):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                perfil = request.user.perfil
                if perfil.empleado.rol == rol:
                    return view_func(request, *args, **kwargs)
            except Perfil.DoesNotExist:
                pass
            return HttpResponseForbidden("No tienes permiso para ver esta página.")
        return _wrapped_view
    return decorador

#FICHAS MASCOTAS

def crear_ficha_mascota(request):
    if request.method == 'POST':
        form = FichaMascotaForm(request.POST)
        if form.is_valid():
            nueva_ficha = form.save(commit=False)
            asistente = Asistente.objects.first() # Obtiene el primer asistente
            if asistente:
                nueva_ficha.asistente = asistente
                nueva_ficha.save()
                return redirect('lista_mascotas')
            else:
                return redirect('lista_mascotas')
    else:
        form = FichaMascotaForm()
    return render(request, 'principal/form_ficha_mascota.html', {'form': form, 'title': 'Crear Ficha'})

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
