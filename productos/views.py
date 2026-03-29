from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            precio=float(request.POST.get('precio') or 0),
            stock=int(request.POST.get('stock') or 0),
            descripcion=request.POST.get('descripcion'),
            imagen=request.FILES.get('imagen')
        )
        return redirect('/productos/')

    return render(request, 'productos/crear.html')


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio = float(request.POST.get('precio') or 0)
        producto.stock = int(request.POST.get('stock') or 0)
        producto.descripcion = request.POST.get('descripcion')

        if request.FILES.get('imagen'):
            producto.imagen = request.FILES.get('imagen')

        producto.save()
        return redirect('/productos/')

    return render(request, 'productos/editar.html', {'producto': producto})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        return redirect('/productos/')

    return render(request, 'productos/eliminar.html', {'producto': producto})