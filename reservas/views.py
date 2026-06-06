from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import Reserva, Compra, DetalleCompra
from canchas.models import Cancha as CanchaDB
from productos.models import Producto as ProductoDB


PRODUCTOS = [
    {"id":1, "nombre":"Balón", "precio":22000, "imagen":"balon1.png", "descripcion":"Balón profesional de futsal"},
    {"id":2, "nombre":"Guayos", "precio":220000, "imagen":"guayos1.jpg", "descripcion":"Guayos para césped sintético"},
    {"id":3, "nombre":"Uniforme", "precio":85000, "imagen":"uniforme22.jpg", "descripcion":"Uniforme deportivo completo"},
    {"id":4, "nombre":"Camiseta Azul fresca", "precio":85000, "imagen":"camisetafutsal.jpg", "descripcion":"Camiseta deportiva fresca"},
    {"id":5, "nombre":"Pantaloneta Blanca", "precio":90000, "imagen":"pantaloneta1.jpg", "descripcion":"Pantaloneta ligera"},
    {"id":6, "nombre":"Pantaloneta Negra", "precio":98000, "imagen":"pantaloneta2.jpg", "descripcion":"Pantaloneta negra"},
    {"id":7, "nombre":"Zapatillas Gamba", "precio":92000, "imagen":"tenisgambeta1.png", "descripcion":"Zapatillas deportivas"},
    {"id":8, "nombre":"Zapatillas Gamba J7", "precio":110000, "imagen":"GAMBETAJ7.png", "descripcion":"Zapatillas profesionales"},
    {"id":9, "nombre":"Balón de Futsal", "precio":105000, "imagen":"BALON1.png", "descripcion":"Balón de futsal profesional"},
    {"id":10, "nombre":"Balón de Fútbol resistente", "precio":105000, "imagen":"BALON2.png", "descripcion":"Balón de fútbol resistente"},
    {"id":11, "nombre":"Medias deportivas", "precio":15000, "imagen":"media1.jpg", "descripcion":"Medias cómodas"},
    {"id":12, "nombre":"Medias de compresión", "precio":18000, "imagen":"media2.jpg", "descripcion":"Medias de compresión"},
    {"id":13, "nombre":"Morral deportivo", "precio":12000, "imagen":"morral1.jpg", "descripcion":"Morral deportivo"},
    {"id":14, "nombre":"Morral profesional", "precio":15000, "imagen":"maleta1.jpg", "descripcion":"Morral profesional"},
    {"id":15, "nombre":"Uniforme Gambeta", "precio":80000, "imagen":"Uniforme-Gambeta.jpg", "descripcion":"Uniforme Gambeta deportivo"},
]


CANCHAS_PUBLICO = [
    {"id":1,"nombre":"Canchas Sintéticas Bogotá Jardin Club","precio":50000,"imagen":"Cancha1.jpg"},
    {"id":2,"nombre":"Canchas Sintéticas Jompibe","precio":60000,"imagen":"cancha2.jpg"},
    {"id":3,"nombre":"Complejo Deportivo Unión Bosa","precio":55000,"imagen":"cancha5.jpg"},
    {"id":4,"nombre":"Cancha La Florida","precio":65000,"imagen":"cancha4.jpg"},
    {"id":5,"nombre":"Club Deportivo Union Bosa","precio":50000,"imagen":"cancha6.jpg"},
    {"id":6,"nombre":"Canchas Futbol Asovivir","precio":70000,"imagen":"cancha11.jpg"},
    {"id":7,"nombre":"Canchas Bosa Santafe","precio":60000,"imagen":"cancha12.jpg"},
    {"id":8,"nombre":"Cancha Sintética Fútbol 5","precio":58000,"imagen":"cancha13.jpg"},
]

MAX_PERSONAS = 50


# ------------------ HOME ------------------
def home(request):
    canchas = CanchaDB.objects.all()[:6]
    productos = ProductoDB.objects.all()[:6]

    if request.user.is_authenticated:
        if request.user.is_superuser:
            rol = "ADMIN"
        elif request.user.is_staff:
            rol = "EMPLEADO"
        else:
            rol = "USUARIO"
    else:
        rol = "INVITADO"

    return render(request, 'home.html', {
        "canchas": canchas,
        "productos": productos,
        "rol": rol
    })


# ------------------ CONTACTO ------------------
def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')

        if nombre and correo and mensaje:
            messages.success(request, "Muchas gracias por contactarnos.")
            return redirect('reservas:contacto')

    return render(request, 'contacto.html')


# ------------------ CANCHAS ------------------
def canchas_publico(request):
    canchas_db = CanchaDB.objects.all()
    return render(request, 'canchas.html', {
        "canchas": CANCHAS_PUBLICO,
        "canchas_db": canchas_db,
    })


# ------------------ DETALLE CANCHA ------------------
def cancha_detalle(request, id):
    cancha = next((c for c in CANCHAS_PUBLICO if c["id"] == id), None)

    if not cancha:
        messages.error(request, "Cancha no encontrada ❌")
        return redirect('reservas:canchas_publico')

    return render(request, 'cancha_detalle.html', {"cancha": cancha})


# ------------------ DETALLE CANCHA BD ------------------
def cancha_detalle_db(request, id):
    from django.shortcuts import get_object_or_404
    cancha = get_object_or_404(CanchaDB, id=id)
    return render(request, 'cancha_detalle_db.html', {"cancha": cancha})


# ------------------ RESERVAR ------------------
def reservar(request, id):
    cancha = next((c for c in CANCHAS_PUBLICO if c["id"] == id), None)

    cancha_db = None
    if not cancha:
        cancha_db = CanchaDB.objects.filter(id=id).first()
        if cancha_db:
            cancha = {
                "id": cancha_db.id,
                "nombre": cancha_db.nombre,
                "precio": int(cancha_db.precio),
                "imagen": cancha_db.imagen.name if cancha_db.imagen else "cancha.jpg",
            }

    if not cancha:
        messages.error(request, "Cancha no encontrada ❌")
        return redirect('reservas:canchas_publico')

    hoy = datetime.now()
    año, mes = hoy.year, hoy.month
    _, total_dias = calendar.monthrange(año, mes)
    dias = list(range(hoy.day, total_dias + 1))

    horarios = ["08:00 AM","10:00 AM","12:00 PM","02:00 PM","04:00 PM","06:00 PM","08:00 PM"]

    if request.method == 'POST':
        dia = request.POST.get('dia')
        horas = request.POST.get('horas')
        personas = request.POST.get('personas')
        horario = request.POST.get('horario')

        if not dia or not horas or not personas or not horario:
            messages.error(request, "Completa todos los campos ❌")
            return redirect(request.path)

        try:
            dia = int(dia)
            horas = int(horas)
            personas = int(personas)
        except ValueError:
            messages.error(request, "Datos inválidos ❌")
            return redirect(request.path)

        if personas < 1:
            messages.error(request, "La cantidad mínima de personas es 1 ❌")
            return redirect(request.path)

        if personas > MAX_PERSONAS:
            messages.error(request, f"La cantidad máxima permitida es {MAX_PERSONAS} personas ❌")
            return redirect(request.path)

        if horas < 1 or horas > 5:
            messages.error(request, "Las horas deben estar entre 1 y 5 ❌")
            return redirect(request.path)

        total = cancha["precio"] * horas
        fecha_str = f"{dia}/{mes}/{año}"

        reserva_obj = Reserva.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            cancha_nombre=cancha["nombre"],
            fecha=fecha_str,
            horario=horario,
            personas=personas,
            horas=horas,
            total=total,
            imagen=cancha["imagen"]
        )

        request.session['reserva'] = {
            "id": reserva_obj.id,
            "cancha": cancha["nombre"],
            "fecha": fecha_str,
            "horario": horario,
            "personas": personas,
            "horas": horas,
            "total": total,
            "imagen": cancha["imagen"]
        }

        return redirect('reservas:confirmacion_reserva')

    return render(request, 'reservar.html', {
        "cancha": cancha,
        "dias": dias,
        "mes": mes,
        "año": año,
        "horarios": horarios
    })


# ------------------ RESERVAR DB ------------------
@login_required
def reservar_db(request, id):
    from django.shortcuts import get_object_or_404
    cancha_db = get_object_or_404(CanchaDB, id=id)
    cancha = {
        "id": cancha_db.id,
        "nombre": cancha_db.nombre,
        "precio": int(cancha_db.precio),
        "imagen": cancha_db.imagen.url if cancha_db.imagen else "cancha.jpg",
    }

    hoy = datetime.now()
    año, mes = hoy.year, hoy.month
    _, total_dias = calendar.monthrange(año, mes)
    dias = list(range(hoy.day, total_dias + 1))
    horarios = ["08:00 AM","10:00 AM","12:00 PM","02:00 PM","04:00 PM","06:00 PM","08:00 PM"]

    if request.method == 'POST':
        dia = request.POST.get('dia')
        horas = request.POST.get('horas')
        personas = request.POST.get('personas')
        horario = request.POST.get('horario')

        if not dia or not horas or not personas or not horario:
            messages.error(request, "Completa todos los campos ❌")
            return redirect(request.path)

        try:
            dia = int(dia)
            horas = int(horas)
            personas = int(personas)
        except ValueError:
            messages.error(request, "Datos inválidos ❌")
            return redirect(request.path)

        if personas < 1 or personas > MAX_PERSONAS:
            messages.error(request, f"Personas debe estar entre 1 y {MAX_PERSONAS} ❌")
            return redirect(request.path)

        if horas < 1 or horas > 5:
            messages.error(request, "Las horas deben estar entre 1 y 5 ❌")
            return redirect(request.path)

        total = cancha["precio"] * horas
        fecha_str = f"{dia}/{mes}/{año}"

        reserva_obj = Reserva.objects.create(
            usuario=request.user,
            cancha_nombre=cancha["nombre"],
            fecha=fecha_str,
            horario=horario,
            personas=personas,
            horas=horas,
            total=total,
            imagen=cancha["imagen"]
        )

        request.session['reserva'] = {
            "id": reserva_obj.id,
            "cancha": cancha["nombre"],
            "fecha": fecha_str,
            "horario": horario,
            "personas": personas,
            "horas": horas,
            "total": total,
            "imagen": cancha["imagen"]
        }

        return redirect('reservas:confirmacion_reserva')

    return render(request, 'reservar.html', {
        "cancha": cancha,
        "dias": dias,
        "mes": mes,
        "año": año,
        "horarios": horarios
    })


# ------------------ CATÁLOGO ------------------
def catalogo(request):
    productos_db = ProductoDB.objects.all()
    return render(request, 'catalogo.html', {"productos": PRODUCTOS, "productos_db": productos_db})


def ver_reserva(request, id):
    reserva = {
        "cancha": request.GET.get("cancha"),
        "fecha": request.GET.get("fecha"),
        "horario": request.GET.get("horario"),
        "personas": request.GET.get("personas"),
        "horas": request.GET.get("horas"),
        "total": request.GET.get("total"),
        "imagen": request.GET.get("imagen"),
    }
    return render(request, 'ver_reserva.html', {"reserva": reserva})


def carrito(request):
    if request.method == 'POST':
        producto_id = int(request.POST.get('productoId', 0))
        cantidad = int(request.POST.get('cantidad', 1))
        source = request.POST.get('source', 'hardcoded')

        producto = None

        if source == 'db':
            producto_db = ProductoDB.objects.filter(id=producto_id).first()
            if producto_db:
                producto = {
                    "id": f"db-{producto_db.id}",
                    "nombre": producto_db.nombre,
                    "precio": float(producto_db.precio),
                    "imagen": producto_db.imagen.url if producto_db.imagen else "",
                }
        else:
            producto = next((p for p in PRODUCTOS if p["id"] == producto_id), None)

        if producto:
            carrito_sesion = request.session.get('carrito', [])
            pid = producto["id"]
            existente = next((p for p in carrito_sesion if p["id"] == pid), None)

            if existente:
                existente["cantidad"] += cantidad
            else:
                carrito_sesion.append({
                    "id": pid,
                    "nombre": producto["nombre"],
                    "precio": producto["precio"],
                    "imagen": producto.get("imagen", ""),
                    "cantidad": cantidad,
                })

            request.session['carrito'] = carrito_sesion
            messages.success(request, f'✅ "{producto["nombre"]}" agregado al carrito')

        return redirect('reservas:carrito')

    carrito_sesion = request.session.get('carrito', [])
    total = sum(p["precio"] * p["cantidad"] for p in carrito_sesion)

    return render(request, 'carrito.html', {
        "carrito": carrito_sesion,
        "total": total
    })


def producto_detalle(request, id):
    producto = next((p for p in PRODUCTOS if p["id"] == id), None)
    return render(request, 'producto.html', {"producto": producto})


def eliminar_del_carrito(request):
    if request.method == 'POST':
        raw_id = request.POST.get('productoId', '0')
        try:
            producto_id = int(raw_id)
        except ValueError:
            producto_id = raw_id
        carrito_sesion = request.session.get('carrito', [])
        carrito_sesion = [p for p in carrito_sesion if p["id"] != producto_id]
        request.session['carrito'] = carrito_sesion
        messages.success(request, 'Producto eliminado del carrito ✅')
    return redirect('reservas:carrito')


def vaciar_carrito(request):
    if request.method == 'POST':
        request.session['carrito'] = []
        messages.success(request, 'Carrito vaciado ✅')
    return redirect('reservas:carrito')


@login_required
def comprar(request):
    if request.method != 'POST':
        return redirect('reservas:carrito')

    carrito_sesion = request.session.get('carrito', [])

    if not carrito_sesion:
        messages.error(request, 'Tu carrito está vacío ❌')
        return redirect('reservas:carrito')

    total = sum(p["precio"] * p["cantidad"] for p in carrito_sesion)

    compra = Compra.objects.create(
        usuario=request.user,
        total=total
    )

    for item in carrito_sesion:
        DetalleCompra.objects.create(
            compra=compra,
            producto_nombre=item["nombre"],
            producto_imagen=item.get("imagen", ""),
            precio=item["precio"],
            cantidad=item["cantidad"]
        )

    request.session['carrito'] = []
    messages.success(request, f'✅ Compra realizada — Factura: {compra.factura}')
    return redirect('reservas:factura', compra_id=compra.id)


@login_required
def factura(request, compra_id):
    compra = Compra.objects.filter(id=compra_id, usuario=request.user).first()

    if not compra:
        messages.error(request, 'Factura no encontrada ❌')
        return redirect('reservas:carrito')

    detalles = compra.detalles.all()

    return render(request, 'factura.html', {
        "compra": compra,
        "detalles": detalles,
    })


# ------------------ PERFIL ------------------
@login_required
def perfil(request):
    from .models import Perfil
    perfil_obj, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'perfil.html', {'perfil': perfil_obj})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '').strip()
        user = request.user

        # ✅ Actualizar nombre de usuario
        if nombre and nombre != user.username:
            if User.objects.filter(username=nombre).exclude(pk=user.pk).exists():
                messages.error(request, 'Ese nombre de usuario ya está en uso ❌')
                return redirect('reservas:perfil')
            user.username = nombre

        # ✅ Actualizar contraseña
        if password:
            import re
            if len(password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres ❌')
                return redirect('reservas:perfil')
            if not re.search(r'[A-Z]', password):
                messages.error(request, 'La contraseña debe tener al menos una mayúscula ❌')
                return redirect('reservas:perfil')
            if not re.search(r'[0-9]', password):
                messages.error(request, 'La contraseña debe tener al menos un número ❌')
                return redirect('reservas:perfil')
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                messages.error(request, 'La contraseña debe tener al menos un carácter especial ❌')
                return redirect('reservas:perfil')
            user.set_password(password)

        user.save()
        update_session_auth_hash(request, user)

        # ✅ Actualizar foto de perfil
        from .models import Perfil
        foto = request.FILES.get('foto')
        if foto:
            perfil_obj, _ = Perfil.objects.get_or_create(user=user)
            perfil_obj.foto = foto
            perfil_obj.save()

        messages.success(request, '✅ Perfil actualizado correctamente')
        return redirect('reservas:perfil')

    return redirect('reservas:perfil')


# ------------------ DASHBOARD ------------------
@login_required
def dashboard(request):
    if request.user.is_superuser:
        rol = "superadmin"
    elif request.user.is_staff:
        rol = "staff"
    else:
        rol = "usuario"

    context = {
        "rol": rol,
        "total_productos": ProductoDB.objects.count(),
        "total_carrito": len(request.session.get("carrito", [])),
        "total_dinero": 0,
        "total_canchas": CanchaDB.objects.count(),
        "total_reservas": Reserva.objects.count(),
    }

    return render(request, "dashboard.html", context)


def confirmar(request):
    reserva = request.session.get('reserva')
    return render(request, 'confirmar.html', {"reserva": reserva})


def confirmacion_reserva(request):
    reserva = request.session.get('reserva')

    if not reserva:
        messages.error(request, "No hay reserva ❌")
        return redirect('reservas:canchas_publico')

    return render(request, 'confirmacion.html', {"reserva": reserva})