from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm
from django.contrib.auth.hashers import make_password

import openpyxl
import os

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# LISTAR USUARIOS
# =========================
@login_required
def lista_usuarios(request):
    # ✅ Solo admin y superusuario pueden ver la lista
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para acceder a esta sección ❌')
        return redirect('reservas:home')

    usuarios = Usuario.objects.all()

    buscar_id = request.GET.get('id')
    buscar_usuario = request.GET.get('usuario')
    buscar_rol = request.GET.get('rol')

    if buscar_id:
        usuarios = usuarios.filter(id__icontains=buscar_id)

    if buscar_usuario:
        usuarios = usuarios.filter(username__icontains=buscar_usuario)

    if buscar_rol:
        usuarios = usuarios.filter(rol=buscar_rol)

    return render(request, 'usuario/lista_usuarios.html', {
        'usuarios': usuarios
    })


# =========================
# CREAR USUARIO
# =========================
@login_required
def crear_usuario(request):
    # ✅ Solo admin y superusuario pueden crear usuarios
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para crear usuarios ❌')
        return redirect('reservas:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        # ✅ Crear en tabla usuarios.Usuario
        Usuario.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            rol=rol
        )

        # ✅ Crear en auth.User para que pueda hacer login
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Asignar permisos según rol
            if rol == 'admin':
                user.is_superuser = True
                user.is_staff = True
            elif rol == 'empleado':
                user.is_staff = True
            user.save()

        messages.success(request, 'Usuario creado correctamente ✅')
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuario/crear_usuario.html')


# =========================
# EDITAR USUARIO
# =========================
@login_required
def editar_usuario(request, id):
    # ✅ Solo admin y superusuario pueden editar usuarios
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para editar usuarios ❌')
        return redirect('reservas:home')

    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente ✅')
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuario/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


# =========================
# ELIMINAR USUARIO
# =========================
@login_required
def eliminar_usuario(request, id):
    # ✅ Solo admin y superusuario pueden eliminar usuarios
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permiso para eliminar usuarios ❌')
        return redirect('reservas:home')

    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuario "{usuario.username}" eliminado ✅')

    return redirect('usuarios:lista_usuarios')


# =========================
# EXPORTAR PDF (PRO 🔥)
# =========================
def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    elementos = []

    # ===== LOGO =====
    ruta_logo = os.path.join('static/img/icono.jpg')  # ajusta si es necesario
    if os.path.exists(ruta_logo):
        logo = Image(ruta_logo, width=80, height=80)
        elementos.append(logo)

    elementos.append(Spacer(1, 10))

    # ===== TITULO =====
    elementos.append(Paragraph("Lista de Usuarios - GoSport", styles['Title']))
    elementos.append(Spacer(1, 20))

    # ===== DATOS =====
    usuarios = Usuario.objects.all()

    data = [["ID", "Usuario", "Email", "Rol"]]

    for u in usuarios:
        data.append([u.id, u.username, u.email, u.rol])

    # ===== TABLA =====
    tabla = Table(data)

    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        ('GRID', (0, 0), (-1, -1), 1, colors.grey),

        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    elementos.append(tabla)

    doc.build(elementos)
    return response


# =========================
# EXPORTAR EXCEL
# =========================
def exportar_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    ws.append(["ID", "Username", "Email", "Rol"])

    for u in Usuario.objects.all():
        ws.append([u.id, u.username, u.email, u.rol])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'

    wb.save(response)
    return response


# =========================
# EXPORTAR TXT
# =========================
def exportar_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="usuarios.txt"'

    for u in Usuario.objects.all():
        response.write(f"{u.id} - {u.username} - {u.email} - {u.rol}\n")

    return response


# =========================
# REPORTE
# =========================
def reporte_reservas(request):
    return render(request, 'reportes/reporte.html')