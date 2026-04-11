from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ✅ IMPORTAR DESDE reservas (CLAVE)
from reservas.models import Cancha, Producto


# 📝 REGISTRO DE USUARIOS
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('auth:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return redirect('auth:register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, 'Usuario creado correctamente')
        return redirect('auth:login')

    return render(request, 'register.html')


# 🔑 LOGIN POR EMAIL
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                login(request, user)

                if user.is_superuser:
                    return redirect('dashboard')  # ✅ corregido
                else:
                    return redirect('home')       # ✅ corregido

            else:
                messages.error(request, 'Correo o contraseña incorrectos')

        except User.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'login.html')


# 🔒 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('auth:login')


# 🏠 HOME PARA USUARIOS NORMALES
@login_required
def home(request):
    canchas = Cancha.objects.all()
    productos = Producto.objects.all()

    context = {
        'canchas': canchas,
        'productos': productos,
        'rol': "ADMIN" if request.user.is_superuser else "USER"
    }

    return render(request, 'home.html', context)


# 👑 DASHBOARD SOLO PARA SUPERADMIN
@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    context = {
        'rol': "Superadmin 👑",
        'total_productos': 0,
        'total_carrito': 0,
        'total_dinero': 0,
        'total_canchas': 0,
    }
    return render(request, 'dashboard.html', context)