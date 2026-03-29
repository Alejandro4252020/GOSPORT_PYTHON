from django.shortcuts import render, redirect
from .models import Cancha

# LISTAR
def lista_canchas(request):
    canchas = Cancha.objects.all()
    return render(request, 'canchas/lista.html', {'canchas': canchas})

# CREAR
def crear_cancha(request):
    if request.method == 'POST':
        Cancha.objects.create(
            nombre=request.POST['nombre'],
            ubicacion=request.POST['ubicacion'],
            precio=request.POST['precio']
        )
        return redirect('lista_canchas')

    return render(request, 'canchas/crear.html')

# EDITAR
def editar_cancha(request, id):
    cancha = Cancha.objects.get(id=id)

    if request.method == 'POST':
        cancha.nombre = request.POST['nombre']
        cancha.ubicacion = request.POST['ubicacion']
        cancha.precio = request.POST['precio']
        cancha.save()
        return redirect('lista_canchas')

    return render(request, 'canchas/editar.html', {'cancha': cancha})

# ELIMINAR
def eliminar_cancha(request, id):
    cancha = Cancha.objects.get(id=id)
    cancha.delete()
    return redirect('lista_canchas')