import io
import pytest
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from canchas.models import Cancha
from productos.models import Producto
from reservas.models import Reserva, Compra, DetalleCompra, Perfil
from usuarios.models import Usuario


# =====================================================
# UTILIDADES
# =====================================================

def imagen_test(nombre="test.jpg"):
    img = Image.new('RGB', (100, 100), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(nombre, buffer.read(), content_type="image/jpeg")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin", email="admin@test.com", password="Admin123!"
    )


@pytest.fixture
def cliente_user(db):
    return User.objects.create_user(
        username="cliente", email="cliente@test.com", password="Cliente123!"
    )


@pytest.fixture
def cancha(db):
    return Cancha.objects.create(
        nombre="Cancha Test", tipo="Futsal", precio=50000,
        capacidad=10, estado="disponible", direccion="Calle 123", imagen=""
    )


@pytest.fixture
def producto(db):
    return Producto.objects.create(
        nombre="Balón Test", precio=22000, stock=10,
        categoria="Deporte", descripcion="Balón de prueba"
    )


# =====================================================
# MODELO CANCHA
# =====================================================

@pytest.mark.django_db
def test_cancha_se_crea_correctamente(cancha):
    assert cancha.nombre == "Cancha Test"
    assert float(cancha.precio) == 50000
    assert cancha.estado == "disponible"


@pytest.mark.django_db
def test_cancha_str(cancha):
    assert str(cancha) == "Cancha Test"


@pytest.mark.django_db
def test_cancha_estados_validos():
    estados = [e[0] for e in Cancha.ESTADOS]
    assert "disponible" in estados
    assert "ocupado" in estados
    assert "mantenimiento" in estados


# =====================================================
# VISTAS CANCHA
# =====================================================

@pytest.mark.django_db
def test_lista_canchas_admin(client, admin_user, cancha):
    client.login(username="admin", password="Admin123!")
    response = client.get(reverse("canchas:lista_canchas"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_lista_canchas_cliente_redirigido(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    response = client.get(reverse("canchas:lista_canchas"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_lista_canchas_sin_login(client):
    response = client.get(reverse("canchas:lista_canchas"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_crear_cancha_admin(client, admin_user):
    client.login(username="admin", password="Admin123!")
    client.post(reverse("canchas:crear_cancha"), {
        "nombre": "Cancha Nueva", "tipo": "Fútbol", "precio": "60000",
        "capacidad": "12", "estado": "disponible", "direccion": "Av. 456",
        "imagen": imagen_test(),
    })
    assert Cancha.objects.filter(nombre="Cancha Nueva").count() == 1


@pytest.mark.django_db
def test_crear_cancha_cliente_denegado(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    client.post(reverse("canchas:crear_cancha"), {
        "nombre": "Cancha Intruso", "tipo": "Fútbol", "precio": "60000",
        "capacidad": "12", "estado": "disponible", "direccion": "Calle Falsa",
    })
    assert Cancha.objects.filter(nombre="Cancha Intruso").count() == 0


@pytest.mark.django_db
def test_editar_cancha_admin(client, admin_user, cancha):
    client.login(username="admin", password="Admin123!")
    client.post(reverse("canchas:editar_cancha", args=[cancha.id]), {
        "nombre": "Cancha Editada", "tipo": "Futsal", "precio": "55000",
        "capacidad": "10", "estado": "ocupado", "direccion": "Nueva Dir",
        "imagen": imagen_test("edit.jpg"),
    })
    cancha.refresh_from_db()
    assert cancha.nombre == "Cancha Editada"


@pytest.mark.django_db
def test_eliminar_cancha_admin(client, admin_user, cancha):
    client.login(username="admin", password="Admin123!")
    client.post(reverse("canchas:eliminar_cancha", args=[cancha.id]))
    assert Cancha.objects.filter(id=cancha.id).count() == 0


@pytest.mark.django_db
def test_eliminar_cancha_cliente_denegado(client, cliente_user, cancha):
    client.login(username="cliente", password="Cliente123!")
    client.post(reverse("canchas:eliminar_cancha", args=[cancha.id]))
    assert Cancha.objects.filter(id=cancha.id).count() == 1


# =====================================================
# MODELO PRODUCTO
# =====================================================

@pytest.mark.django_db
def test_producto_se_crea_correctamente(producto):
    assert producto.nombre == "Balón Test"
    assert producto.precio == 22000
    assert producto.stock == 10


@pytest.mark.django_db
def test_producto_str(producto):
    assert str(producto) == "Balón Test"


@pytest.mark.django_db
def test_producto_sin_imagen(producto):
    assert not producto.imagen


# =====================================================
# MODELO RESERVA
# =====================================================

@pytest.mark.django_db
def test_reserva_se_crea_correctamente(cliente_user):
    reserva = Reserva.objects.create(
        usuario=cliente_user,
        cancha_nombre="Cancha Test",
        fecha="13/06/2026",
        horario="08:00 AM",
        personas=5,
        horas=2,
        total=100000,
    )
    assert reserva.cancha_nombre == "Cancha Test"
    assert reserva.total == 100000
    assert reserva.usuario == cliente_user


@pytest.mark.django_db
def test_reserva_str(cliente_user):
    reserva = Reserva.objects.create(
        usuario=cliente_user,
        cancha_nombre="Cancha ABC",
        fecha="13/06/2026",
        horario="10:00 AM",
        personas=3,
        horas=1,
        total=50000,
    )
    assert "Cancha ABC" in str(reserva)
    assert "13/06/2026" in str(reserva)


# =====================================================
# MODELO COMPRA
# =====================================================

@pytest.mark.django_db
def test_compra_genera_factura(cliente_user):
    compra = Compra.objects.create(usuario=cliente_user, total=50000)
    assert compra.factura.startswith("GS-")
    assert len(compra.factura) == 11


@pytest.mark.django_db
def test_compra_str(cliente_user):
    compra = Compra.objects.create(usuario=cliente_user, total=50000)
    assert "cliente" in str(compra)
    assert "GS-" in str(compra)


@pytest.mark.django_db
def test_detalle_compra_subtotal(cliente_user):
    compra = Compra.objects.create(usuario=cliente_user, total=0)
    detalle = DetalleCompra.objects.create(
        compra=compra,
        producto_nombre="Balón",
        precio=22000,
        cantidad=3
    )
    assert detalle.subtotal == 66000


# =====================================================
# MODELO PERFIL
# =====================================================

@pytest.mark.django_db
def test_perfil_se_crea_con_usuario(cliente_user):
    perfil = Perfil.objects.get(user=cliente_user)
    assert perfil.user == cliente_user


@pytest.mark.django_db
def test_perfil_str(cliente_user):
    perfil = Perfil.objects.get(user=cliente_user)
    assert str(perfil) == "cliente"


# =====================================================
# VISTAS AUTH
# =====================================================

@pytest.mark.django_db
def test_register_exitoso(client):
    client.post(reverse("auth:register"), {
        "username": "nuevo",
        "email": "nuevo@test.com",
        "password": "Nuevo1234!",
        "password2": "Nuevo1234!",
    })
    assert User.objects.filter(username="nuevo").exists()


@pytest.mark.django_db
def test_register_passwords_no_coinciden(client):
    client.post(reverse("auth:register"), {
        "username": "nuevo2",
        "email": "nuevo2@test.com",
        "password": "Nuevo1234!",
        "password2": "Diferente1!",
    })
    assert not User.objects.filter(username="nuevo2").exists()


@pytest.mark.django_db
def test_register_password_corta(client):
    client.post(reverse("auth:register"), {
        "username": "nuevo3",
        "email": "nuevo3@test.com",
        "password": "abc",
        "password2": "abc",
    })
    assert not User.objects.filter(username="nuevo3").exists()


@pytest.mark.django_db
def test_register_usuario_duplicado(client, cliente_user):
    client.post(reverse("auth:register"), {
        "username": "cliente",
        "email": "otro@test.com",
        "password": "Nuevo1234!",
        "password2": "Nuevo1234!",
    })
    assert User.objects.filter(username="cliente").count() == 1


@pytest.mark.django_db
def test_login_exitoso(client, cliente_user):
    response = client.post(reverse("auth:login"), {
        "email": "cliente@test.com",
        "password": "Cliente123!",
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_credenciales_incorrectas(client):
    response = client.post(reverse("auth:login"), {
        "email": "noexiste@test.com",
        "password": "mal",
    })
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_requiere_login(client):
    response = client.get(reverse("auth:home"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_solo_admin(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    response = client.get(reverse("auth:dashboard"))
    assert response.status_code == 302


# =====================================================
# VISTAS RESERVAS
# =====================================================

@pytest.mark.django_db
def test_home_publico(client):
    response = client.get(reverse("reservas:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_catalogo_publico(client):
    response = client.get(reverse("reservas:catalogo"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_canchas_publico(client):
    response = client.get(reverse("reservas:canchas_publico"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_carrito_con_login(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    response = client.get(reverse("reservas:carrito"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_comprar_requiere_login(client):
    response = client.post(reverse("reservas:comprar"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_perfil_requiere_login(client):
    response = client.get(reverse("reservas:perfil"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_reservar_db_requiere_login(client, cancha):
    response = client.get(reverse("reservas:reservar_db", args=[cancha.id]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_comprar_con_carrito(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    session = client.session
    session['carrito'] = [{"id": 1, "nombre": "Balón", "precio": 22000, "imagen": "", "cantidad": 2}]
    session.save()
    client.post(reverse("reservas:comprar"))
    assert Compra.objects.filter(usuario=cliente_user).count() == 1


# =====================================================
# VISTAS USUARIOS
# =====================================================

@pytest.mark.django_db
def test_lista_usuarios_admin(client, admin_user):
    client.login(username="admin", password="Admin123!")
    response = client.get(reverse("usuarios:lista_usuarios"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_lista_usuarios_cliente_redirigido(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    response = client.get(reverse("usuarios:lista_usuarios"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_eliminar_usuario_admin(client, admin_user):
    client.login(username="admin", password="Admin123!")
    u = Usuario.objects.create(
        username="borrar", email="borrar@test.com",
        password="x", rol="cliente"
    )
    client.post(reverse("usuarios:eliminar_usuario", args=[u.id]))
    assert Usuario.objects.filter(id=u.id).count() == 0


@pytest.mark.django_db
def test_eliminar_usuario_cliente_denegado(client, cliente_user):
    client.login(username="cliente", password="Cliente123!")
    u = Usuario.objects.create(
        username="borrar2", email="borrar2@test.com",
        password="x", rol="cliente"
    )
    client.post(reverse("usuarios:eliminar_usuario", args=[u.id]))
    assert Usuario.objects.filter(id=u.id).count() == 1