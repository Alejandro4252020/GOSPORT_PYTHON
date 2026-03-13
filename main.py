from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# -------------------------
# BASE DE DATOS SIMULADA
# -------------------------

productos_db = [
    {"id":1,"nombre":"Camiseta deportiva","precio":85000,"imagen":"camisetafutsal.jpg"},
    {"id":2,"nombre":"Uniforme Gambeta","precio":80000,"imagen":"Uniforme-Gambeta.jpg"},
    {"id":3,"nombre":"Pantaloneta blanca","precio":90000,"imagen":"pantaloneta1.jpg"},
    {"id":4,"nombre":"Zapatillas Gamba","precio":92000,"imagen":"tenisgambeta1.png"},
    {"id":5,"nombre":"Balón Futsal","precio":105000,"imagen":"BALON1.png"}
]

# carrito en memoria
carrito = []


# -------------------------
# HOME
# -------------------------

@app.get("/")
async def home(request: Request):

    canchas = [
        {
            "id":1,
            "nombre":"Cancha 1",
            "estado":"Disponible",
            "imagen":"cancha1.jpg",
            "descripcion":"Cancha sintética profesional",
            "direccion":"Bogotá Bosa"
        },
        {
            "id":2,
            "nombre":"Cancha 2",
            "estado":"Ocupada",
            "imagen":"cancha2.jpg",
            "descripcion":"Cancha cubierta",
            "direccion":"Bogotá Centro"
        }
    ]

    productos = [
        {"id":1,"nombre":"Balón","precio":80000,"imagen":"BALON1.png"},
        {"id":2,"nombre":"Guayos","precio":220000,"imagen":"tenisgambeta1.png"}
    ]

    return templates.TemplateResponse("home.html", {
        "request": request,
        "rol": "USER",
        "canchas": canchas,
        "productos": productos
    })


# -------------------------
# LISTA DE CANCHAS
# -------------------------




# -------------------------
# DETALLE DE CANCHA
# -------------------------

@app.get("/canchas")
async def lista_canchas(request: Request):  # noqa: F811

    canchas = [
        {
            "id":1,
            "nombre":"Canchas Sintéticas Bogotá Jardin Club",
            "estado":"Disponible",
            "imagen":"cancha1.jpg",
            "descripcion":"Cancha sintética profesional",
            "direccion":"Bogotá Bosa"
        },
        {
            "id":2,
            "nombre":"Canchas Sinteticas Jompibe",
            "estado":"Disponible",
            "imagen":"cancha2.jpg",
            "descripcion":"Cancha cubierta",
            "direccion":"Bogotá"
        },
        {
            "id":3,
            "nombre":"Complejo Deportivo Unión Bosa",
            "estado":"Disponible",
            "imagen":"cancha3.jpg",
            "descripcion":"Cancha sintética",
            "direccion":"Bogotá"
        },
        {
            "id":4,
            "nombre":"Cancha La Florida",
            "estado":"Disponible",
            "imagen":"cancha4.jpg",
            "descripcion":"Cancha sintética",
            "direccion":"Bogotá"
        },
        {
            "id":5,
            "nombre":"Club Deportivo Union Bosa",
            "estado":"Disponible",
            "imagen":"cancha5.jpg",
            "descripcion":"Cancha sintética",
            "direccion":"Bogotá"
        },
        {
            "id":6,
            "nombre":"Cachas Futbol Asovivir",
            "estado":"Disponible",
            "imagen":"cancha6.jpg",
            "descripcion":"Cancha sintética",
            "direccion":"Bogotá"
        },
        {
    "id":7,
    "nombre":"Canchas Bosa Santafe",
    "estado":"Disponible",
    "imagen":"canchabosa.jpg",
    "descripcion":"Cancha sintética",
    "direccion":"Bogotá Bosa"
},
{
    "id":8,
    "nombre":"Cancha Sintética de Fútbol 5",
    "estado":"Disponible",
    "imagen":"cancha.jpg",
    "descripcion":"Cancha sintética de fútbol 5",
    "direccion":"Bogotá"
}
    ]

    return templates.TemplateResponse("canchas.html", {
        "request": request,
        "canchas": canchas
    })


# -------------------------
# CATALOGO (TIENDA)
# -------------------------

@app.get("/catalogo")
async def catalogo(request: Request):

    return templates.TemplateResponse("catalogo.html", {
        "request": request,
        "productos": productos_db
    })


# -------------------------
# AGREGAR AL CARRITO
# -------------------------

@app.post("/carrito/agregar")
async def agregar_carrito(
    productoId: int = Form(...),
    cantidad: int = Form(1)
):

    for item in carrito:
        if item["productoId"] == productoId:
            item["cantidad"] += 1
            return RedirectResponse("/carrito", status_code=303)

    carrito.append({
        "productoId": productoId,
        "cantidad": 1
    })

    return RedirectResponse("/carrito", status_code=303)


# -------------------------
# VER CARRITO
# -------------------------

@app.get("/carrito")
async def ver_carrito(request: Request):

    productos = {p["id"]: p for p in productos_db}

    total = 0

    for item in carrito:
        producto = productos.get(item["productoId"])

        if producto:
            total += producto["precio"] * item["cantidad"]

    return templates.TemplateResponse("carrito.html", {
        "request": request,
        "carrito": carrito,
        "productos": productos,
        "total": total
    })


# -------------------------
# REDUCIR CANTIDAD
# -------------------------

@app.post("/carrito/reducir")
async def reducir(productoId: int = Form(...)):

    for item in carrito:

        if item["productoId"] == productoId:

            if item["cantidad"] > 1:
                item["cantidad"] -= 1
            else:
                carrito.remove(item)

            break

    return RedirectResponse("/carrito", status_code=303)


# -------------------------
# ELIMINAR PRODUCTO
# -------------------------

@app.post("/carrito/eliminar")
async def eliminar(productoId: int = Form(...)):

    for item in carrito:
        if item["productoId"] == productoId:
            carrito.remove(item)
            break

    return RedirectResponse("/carrito", status_code=303)


# -------------------------
# VACIAR CARRITO
# -------------------------

@app.post("/carrito/vaciar")
async def vaciar():

    carrito.clear()

    return RedirectResponse("/carrito", status_code=303)
@app.get("/producto/{producto_id}")
async def detalle_producto(request: Request, producto_id: int):

    producto = next((p for p in productos_db if p["id"] == producto_id), None)

    if not producto:
        return {"error": "Producto no encontrado"}

    return templates.TemplateResponse(
        "detalle_producto.html",
        {
            "request": request,
            "producto": producto
        }
    )
@app.get("/perfil")
async def perfil(request: Request):

    usuario = {
        "nombre": "Juan Pérez",
        "email": "juan@gmail.com",
        "telefono": "3001234567",
        "direccion": "Bogotá"
    }

    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario": usuario
    })