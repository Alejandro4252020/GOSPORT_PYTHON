from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto


# ===== LISTAR =====
@login_required
def lista_productos(request):
    # ✅ Solo admin y empleado pueden acceder al CRUD
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para acceder a esta sección ❌')
        return redirect('reservas:home')

    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})


# ===== CREAR =====
@login_required
def crear_producto(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para crear productos ❌')
        return redirect('reservas:home')

    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            precio=float(request.POST.get('precio') or 0),
            stock=int(request.POST.get('stock') or 0),
            categoria=request.POST.get('categoria'),
            descripcion=request.POST.get('descripcion'),
            imagen=request.FILES.get('imagen')
        )
        messages.success(request, 'Producto creado correctamente ✅')
        return redirect('productos:lista_productos')

    return render(request, 'productos/crear.html')


# ===== EDITAR =====
@login_required
def editar_producto(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para editar productos ❌')
        return redirect('reservas:home')

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio = float(request.POST.get('precio') or 0)
        producto.stock = int(request.POST.get('stock') or 0)
        producto.categoria = request.POST.get('categoria')
        producto.descripcion = request.POST.get('descripcion')

        if request.FILES.get('imagen'):
            producto.imagen = request.FILES.get('imagen')

        producto.save()
        messages.success(request, 'Producto actualizado correctamente ✅')
        return redirect('productos:lista_productos')

    return render(request, 'productos/editar.html', {'producto': producto})

# ===== HABILITAR / DESHABILITAR (solo POST) =====
@login_required
def eliminar_producto(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para modificar productos ❌')
        return redirect('reservas:home')

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.activo = not producto.activo
        producto.save()
        estado = 'habilitado' if producto.activo else 'deshabilitado'
        messages.success(request, f'Producto "{producto.nombre}" {estado} correctamente ✅')

    return redirect('productos:lista_productos')