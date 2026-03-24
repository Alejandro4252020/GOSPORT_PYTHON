from django.shortcuts import render

def home(request):

    canchas = [
        {"id":1, "nombre":"Cancha 1", "estado":"Disponible", "imagen":"cancha1.jpg"},
        {"id":2, "nombre":"Cancha 2", "estado":"Ocupada", "imagen":"cancha2.jpg"},
        {"id":3, "nombre":"Cancha 3", "estado":"Disponible", "imagen":"canchabosa.jpg"},
    ]

    productos = [
        {"id":1, "nombre":"Balón", "precio":"22000", "imagen":"balon1.png"},
        {"id":2, "nombre":"Guayos", "precio":"220000", "imagen":"guayos1.jpg"},
    ]

    return render(request, 'home.html', {
        "canchas": canchas,
        "productos": productos
    })


def canchas(request):
    # Lista completa de 14 canchas
    canchas = [
        {"id":1,"nombre":"Canchas Sintéticas Bogotá Jardin Club","estado":"Disponible","imagen":"cancha1.jpg","descripcion":"Cancha sintética profesional","direccion":"Bogotá Bosa"},
        {"id":2,"nombre":"Canchas Sintéticas Jompibe","estado":"Disponible","imagen":"cancha2.jpg","descripcion":"Cancha cubierta","direccion":"Bogotá"},
        {"id":3,"nombre":"Complejo Deportivo Unión Bosa","estado":"Disponible","imagen":"cancha14.jpg","descripcion":"Cancha sintética","direccion":"Bogotá"},
        {"id":4,"nombre":"Cancha La Florida","estado":"Disponible","imagen":"cancha4.jpg","descripcion":"Cancha sintética","direccion":"Bogotá"},
        {"id":5,"nombre":"Club Deportivo Union Bosa","estado":"Disponible","imagen":"cancha5.jpg","descripcion":"Cancha sintética","direccion":"Bogotá"},
        {"id":6,"nombre":"Canchas Futbol Asovivir","estado":"Disponible","imagen":"cancha6.jpg","descripcion":"Cancha sintética","direccion":"Bogotá"},
        {"id":7,"nombre":"Canchas Bosa Santafe","estado":"Disponible","imagen":"canchabosa.jpg","descripcion":"Cancha sintética","direccion":"Bogotá Bosa"},
        {"id":8,"nombre":"Cancha Sintética de Fútbol 5","estado":"Disponible","imagen":"cancha.jpg","descripcion":"Cancha sintética de fútbol 5","direccion":"Bogotá"},
       
    ]

    return render(request, 'canchas.html', {"canchas": canchas})
def catalogo(request):
    return render(request, 'catalogo.html')

def perfil(request):
    return render(request, 'perfil.html')

def carrito(request):
    return render(request, 'carrito.html')