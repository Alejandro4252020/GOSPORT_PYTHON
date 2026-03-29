from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table


# LISTA
def lista_usuarios(request):
    usuarios = Usuario.objects.all()

    # filtros
    id_buscar = request.GET.get('id')
    username = request.GET.get('username')
    rol = request.GET.get('rol')

    if id_buscar:
        usuarios = usuarios.filter(id=id_buscar)

    if username:
        usuarios = usuarios.filter(username__icontains=username)

    if rol and rol != '-- Todos --':
        usuarios = usuarios.filter(rol=rol)

    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

# CREAR
def crear_usuario(request):
    if request.method == 'POST':
        Usuario.objects.create(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            rol=request.POST.get('rol'),
            password=make_password(request.POST.get('password'))  # 🔐 IMPORTANTE
        )
        return redirect('lista_usuarios')

    return render(request, 'usuarios/crear.html')


# EDITAR
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.rol = request.POST.get('rol')

        password = request.POST.get('password')
        if password:
            usuario.password = make_password(password)  # 🔐 solo si cambia

        usuario.save()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/editar.html', {'usuario': usuario})


# ELIMINAR
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

# EXPORTAR PDF
def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'

    doc = SimpleDocTemplate(response)

    usuarios = Usuario.objects.all()

    data = [['ID', 'Username', 'Rol']]

    for u in usuarios:
        data.append([u.id, u.username, u.rol])

    table = Table(data)

    doc.build([table])

    return response


# EXPORTAR EXCEL
def exportar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    ws.append(['ID', 'Username', 'Rol'])

    usuarios = Usuario.objects.all()
    for u in usuarios:
        ws.append([u.id, u.username, u.rol])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=usuarios.xlsx'

    wb.save(response)
    return response


# EXPORTAR TXT
def exportar_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=usuarios.txt'

    usuarios = Usuario.objects.all().order_by('id')

    for u in usuarios:
        response.write(f"{u.id} - {u.username} - {u.rol}\n")

    return response