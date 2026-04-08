from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# 📝 REGISTRO DE USUARIOS
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        # Validaciones
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return redirect('register')

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, 'Usuario creado correctamente')
        return redirect('login')

    return render(request, 'register.html')


# 🔑 LOGIN POR EMAIL
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        try:
            # Buscar usuario por email
            user = User.objects.get(email=email)

            # Validar contraseña
            if user.check_password(password):
                login(request, user)  # Login exitoso

                # Redirección según rol
                if user.is_superuser:
                    return redirect('dashboard/')  # Superadmin al dashboard/
                else:
                    return redirect('home/')  # Usuario normal al home/

            else:
                messages.error(request, 'Correo o contraseña incorrectos')

        except User.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'login.html')


# 🔒 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 🏠 HOME PARA USUARIOS NORMALES
@login_required
def home(request):
    return render(request, 'home.html')


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