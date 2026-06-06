from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from canchas.models import Cancha
from productos.models import Producto
from usuarios.models import Usuario


# 📝 REGISTRO
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # ✅ Campos vacíos
        if not email or not username or not password:
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('auth:register')

        # ✅ Contraseñas coinciden
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('auth:register')

        # ✅ Longitud mínima
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('auth:register')

        # ✅ Usuario existente
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('auth:register')

        # ✅ Correo existente
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return redirect('auth:register')

        # ✅ Crear en auth.User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ✅ Crear en usuarios.Usuario (sincronización)
        Usuario.objects.create(
            username=username,
            email=email,
            password=user.password,  # Ya hasheado
            rol='cliente'
        )

        messages.success(request, 'Cuenta creada correctamente ✅')
        return redirect('auth:login')

    return render(request, 'register.html')


# 🔑 LOGIN
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        try:
            user = User.objects.filter(email=email).first()

            if user is None:
                raise User.DoesNotExist

            if user.check_password(password):
                login(request, user)

                # ✅ admin y empleado → dashboard, cliente → home
                if user.is_superuser or user.is_staff:
                    return redirect('auth:dashboard')
                else:
                    return redirect('auth:home')

            else:
                messages.error(request, 'Correo o contraseña incorrectos')

        except User.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'login.html')


# 🔒 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('auth:login')


# 🏠 HOME
@login_required
def home(request):
    canchas = Cancha.objects.all()
    productos = Producto.objects.all()

    context = {
        'canchas': canchas,
        'productos': productos,
        'rol': "ADMIN" if request.user.is_superuser else ("EMPLEADO" if request.user.is_staff else "USER")
    }

    return render(request, 'home.html', context)

# 👑 DASHBOARD
@login_required
def dashboard(request):
    # ✅ Admin y empleado pueden ver el dashboard
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('auth:home')

    context = {
        'rol': "Superadmin 👑" if request.user.is_superuser else "Empleado",
        'total_productos': Producto.objects.count(),
        'total_canchas': Cancha.objects.count(),
        'total_carrito': 0,
        'total_dinero': 0,
    }

    return render(request, 'dashboard.html', context)