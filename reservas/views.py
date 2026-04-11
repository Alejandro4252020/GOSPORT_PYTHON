from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import calendar
from django.contrib.auth.decorators import login_required


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


# ------------------ HOME ------------------
def home(request):
    canchas = [
        {"id":1, "nombre":"Cancha 1", "estado":"Disponible", "imagen":"cancha1.jpg"},
        {"id":2, "nombre":"Cancha 2", "estado":"Ocupada", "imagen":"cancha2.jpg"},
        {"id":3, "nombre":"Cancha 3", "estado":"Disponible", "imagen":"canchabosa.jpg"},
    ]

    productos_destacados = [
        PRODUCTOS[0],
        PRODUCTOS[1],
        PRODUCTOS[2],
    ]

    if request.user.is_authenticated:
        if request.user.is_superuser:
            rol = "ADMIN"
        else:
            rol = "USUARIO"
    else:
        rol = "INVITADO"

    return render(request, 'home.html', {
        "canchas": canchas,
        "productos": productos_destacados,
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
            return redirect('contacto')

    return render(request, 'contacto.html')


# ------------------ CANCHAS ------------------
def canchas(request):
    canchas = [
        {"id":1,"nombre":"Canchas Sintéticas Bogotá Jardin Club","precio":50000,"imagen":"Cancha1.jpg"},
        {"id":2,"nombre":"Canchas Sintéticas Jompibe","precio":60000,"imagen":"cancha2.jpg"},
        {"id":3,"nombre":"Complejo Deportivo Unión Bosa","precio":55000,"imagen":"cancha5.jpg"},
        {"id":4,"nombre":"Cancha La Florida","precio":65000,"imagen":"cancha4.jpg"},
        {"id":5,"nombre":"Club Deportivo Union Bosa","precio":50000,"imagen":"cancha6.jpg"},
        {"id":6,"nombre":"Canchas Futbol Asovivir","precio":70000,"imagen":"cancha11.jpg"},
        {"id":7,"nombre":"Canchas Bosa Santafe","precio":60000,"imagen":"cancha12.jpg"},
        {"id":8,"nombre":"Cancha Sintética Fútbol 5","precio":58000,"imagen":"cancha13.jpg"},
    ]

    return render(request, 'canchas.html', {"canchas": canchas})


# ------------------ DETALLE CANCHA ------------------
def cancha_detalle(request, id):
    canchas = [
        {"id":1,"nombre":"Canchas Sintéticas Bogotá Jardin Club","precio":50000,"imagen":"Cancha1.jpg"},
        {"id":2,"nombre":"Canchas Sintéticas Jompibe","precio":60000,"imagen":"cancha2.jpg"},
        {"id":3,"nombre":"Complejo Deportivo Unión Bosa","precio":55000,"imagen":"cancha5.jpg"},
        {"id":4,"nombre":"Cancha La Florida","precio":65000,"imagen":"cancha4.jpg"},
        {"id":5,"nombre":"Club Deportivo Union Bosa","precio":50000,"imagen":"cancha6.jpg"},
        {"id":6,"nombre":"Canchas Futbol Asovivir","precio":70000,"imagen":"cancha11.jpg"},
        {"id":7,"nombre":"Canchas Bosa Santafe","precio":60000,"imagen":"cancha12.jpg"},
        {"id":8,"nombre":"Cancha Sintética Fútbol 5","precio":58000,"imagen":"cancha13.jpg"},
    ]

    cancha = next((c for c in canchas if c["id"] == id), None)

    if not cancha:
        messages.error(request, "Cancha no encontrada ❌")
        return redirect('canchas')

    return render(request, 'cancha_detalle.html', {"cancha": cancha})


# ------------------ RESERVAR ------------------
def reservar(request, id):
    canchas = [
        {"id":1,"nombre":"Canchas Sintéticas Bogotá Jardin Club","precio":50000,"imagen":"Cancha1.jpg"},
        {"id":2,"nombre":"Canchas Sintéticas Jompibe","precio":60000,"imagen":"cancha2.jpg"},
        {"id":3,"nombre":"Complejo Deportivo Unión Bosa","precio":55000,"imagen":"cancha5.jpg"},
        {"id":4,"nombre":"Cancha La Florida","precio":65000,"imagen":"cancha4.jpg"},
        {"id":5,"nombre":"Club Deportivo Union Bosa","precio":50000,"imagen":"cancha6.jpg"},
        {"id":6,"nombre":"Canchas Futbol Asovivir","precio":70000,"imagen":"cancha11.jpg"},
        {"id":7,"nombre":"Canchas Bosa Santafe","precio":60000,"imagen":"cancha12.jpg"},
        {"id":8,"nombre":"Cancha Sintética Fútbol 5","precio":58000,"imagen":"cancha13.jpg"},
    ]

    cancha = next((c for c in canchas if c["id"] == id), None)

    if not cancha:
        messages.error(request, "Cancha no encontrada ❌")
        return redirect('canchas')

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

        total = cancha["precio"] * horas

        request.session['reserva'] = {
            "cancha": cancha["nombre"],
            "fecha": f"{dia}/{mes}/{año}",
            "horario": horario,
            "personas": personas,
            "horas": horas,
            "total": total,
            "imagen": cancha["imagen"]
        }

        return redirect('confirmacion_reserva')

    return render(request, 'reservar.html', {
        "cancha": cancha,
        "dias": dias,
        "mes": mes,
        "año": año,
        "horarios": horarios
    })


# ------------------ RESTO ------------------
def catalogo(request):
    return render(request, 'catalogo.html', {"productos": PRODUCTOS})


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
    request.session['carrito'] = []
    return redirect('carrito')


def vaciar_carrito(request):
    request.session['carrito'] = []
    return redirect('carrito')


def perfil(request):
    return render(request, 'perfil.html')


def editar_perfil(request):
    return redirect('perfil')


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
        "total_productos": len(PRODUCTOS),
        "total_carrito": len(request.session.get("carrito", [])),
        "total_dinero": 0,
        "total_canchas": 8,
    }

    return render(request, "dashboard.html", context)


def confirmar(request):
    reserva = request.session.get('reserva')
    return render(request, 'confirmar.html', {"reserva": reserva})


def confirmacion_reserva(request):
    reserva = request.session.get('reserva')

    if not reserva:
        messages.error(request, "No hay reserva ❌")
        return redirect('canchas')

    return render(request, 'confirmacion.html', {"reserva": reserva})