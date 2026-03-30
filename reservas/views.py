from django.shortcuts import render, redirect

# ------------------ LISTA MAESTRA DE PRODUCTOS ------------------
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

    # Productos destacados: Balón → Guayos → Uniforme
    productos_destacados = [
        next(p for p in PRODUCTOS if p["imagen"] == "balon1.png"),
        next(p for p in PRODUCTOS if p["imagen"] == "guayos1.jpg"),
        next(p for p in PRODUCTOS if p["imagen"] == "uniforme22.jpg"),
    ]

    return render(request, 'home.html', {
        "canchas": canchas,
        "productos": productos_destacados
    })

# ------------------ CANCHAS ------------------
def canchas(request):
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

# ------------------ DETALLE CANCHA ------------------
def cancha_detalle(request, id):
    canchas = [
        {"id":1,"nombre":"Canchas Sintéticas Bogotá Jardin Club","estado":"Disponible","imagen":"cancha1.jpg","descripcion":"Cancha sintética profesional","direccion":"Bogotá Bosa","precio":50000},
        {"id":2,"nombre":"Canchas Sintéticas Jompibe","estado":"Disponible","imagen":"cancha2.jpg","descripcion":"Cancha cubierta","direccion":"Bogotá","precio":60000},
        {"id":3,"nombre":"Complejo Deportivo Unión Bosa","estado":"Disponible","imagen":"cancha14.jpg","descripcion":"Cancha sintética","direccion":"Bogotá","precio":55000},
        {"id":4,"nombre":"Cancha La Florida","estado":"Disponible","imagen":"cancha4.jpg","descripcion":"Cancha sintética","direccion":"Bogotá","precio":40000},
        {"id":5,"nombre":"Club Deportivo Union Bosa","estado":"Disponible","imagen":"cancha5.jpg","descripcion":"Cancha sintética","direccion":"Bogotá","precio":45000},
        {"id":6,"nombre":"Canchas Futbol Asovivir","estado":"Disponible","imagen":"cancha6.jpg","descripcion":"Cancha sintética","direccion":"Bogotá","precio":50000},
        {"id":7,"nombre":"Canchas Bosa Santafe","estado":"Disponible","imagen":"canchabosa.jpg","descripcion":"Cancha sintética","direccion":"Bogotá Bosa","precio":35000},
        {"id":8,"nombre":"Cancha Sintética de Fútbol 5","estado":"Disponible","imagen":"cancha.jpg","descripcion":"Cancha sintética de fútbol 5","direccion":"Bogotá","precio":30000},
    ]

    cancha = next((c for c in canchas if c["id"] == id), None)
    return render(request, 'cancha_detalle.html', {"cancha": cancha})

# ------------------ RESERVAR ------------------
def reservar(request, id):
    if request.method == 'POST':
        horas = request.POST.get('horas')
        print(f"Reserva cancha {id} por {horas} horas")
        return redirect('/canchas/')

# ------------------ CATALOGO ------------------
def catalogo(request):
    return render(request, 'catalogo.html')

# ------------------ PERFIL ------------------
def perfil(request):
    return render(request, 'perfil.html')

# ------------------ EDITAR PERFIL ------------------
def editar_perfil(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        request.session['nombre'] = nombre
        return redirect('/perfil/')

# ------------------ CARRITO ------------------
def carrito(request):
    if request.method == 'POST':
        try:
            producto_id = int(request.POST.get('productoId', 0))
        except ValueError:
            producto_id = 0

        cantidad = int(request.POST.get('cantidad', 1))

        producto = next((p for p in PRODUCTOS if p["id"] == producto_id), None)

        if producto:
            carrito_sesion = request.session.get('carrito', [])
            carrito_sesion.append({
                "id": producto["id"],
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "imagen": producto["imagen"],
                "cantidad": cantidad
            })
            request.session['carrito'] = carrito_sesion

        return redirect('/carrito/')

    carrito_sesion = request.session.get('carrito', [])

    # 🔥 CALCULAR TOTAL
    total = sum(p["precio"] * p["cantidad"] for p in carrito_sesion)

    return render(request, 'carrito.html', {
        "carrito": carrito_sesion,
        "total": total
    })
# ------------------ PRODUCTO DETALLE ------------------
def producto_detalle(request, id):
    producto = next((p for p in PRODUCTOS if p["id"] == id), None)
    return render(request, 'producto.html', {"producto": producto})

# ------------------ ELIMINAR DEL CARRITO ------------------
def eliminar_del_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('productoId')
        carrito_sesion = request.session.get('carrito', [])
        carrito_sesion = [p for p in carrito_sesion if str(p["id"]) != str(producto_id)]
        request.session['carrito'] = carrito_sesion
    return redirect('/carrito/')

# ------------------ VACÍAR CARRITO ------------------
def vaciar_carrito(request):
    if request.method == 'POST':
        request.session['carrito'] = []
    return redirect('/carrito/')