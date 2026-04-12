from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cancha
from .forms import CanchaForm


# LISTAR
@login_required
def lista_canchas(request):
    # ✅ Solo admin y empleado pueden acceder al CRUD
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para acceder a esta sección ❌')
        return redirect('reservas:home')

    canchas = Cancha.objects.all()
    return render(request, 'canchas/lista_canchas.html', {
        'canchas': canchas
    })


# CREAR
@login_required
def crear_cancha(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para crear canchas ❌')
        return redirect('reservas:home')

    form = CanchaForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cancha creada correctamente ✅')
        return redirect('canchas:lista_canchas')

    return render(request, 'canchas/crear_cancha.html', {
        'form': form
    })


# EDITAR
@login_required
def editar_cancha(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para editar canchas ❌')
        return redirect('reservas:home')

    cancha = get_object_or_404(Cancha, id=id)
    form = CanchaForm(request.POST or None, request.FILES or None, instance=cancha)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cancha actualizada correctamente ✅')
        return redirect('canchas:lista_canchas')

    return render(request, 'canchas/editar_cancha.html', {
        'form': form
    })


# ELIMINAR (solo POST)
@login_required
def eliminar_cancha(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para eliminar canchas ❌')
        return redirect('reservas:home')

    cancha = get_object_or_404(Cancha, id=id)

    if request.method == 'POST':
        nombre = cancha.nombre
        cancha.delete()
        messages.success(request, f'Cancha "{nombre}" eliminada ✅')

    return redirect('canchas:lista_canchas')