from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from productos.models import Producto


class ProductoModelTest(TestCase):

    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Balón Test", precio=22000, stock=10,
            categoria="Deportes", descripcion="Balón profesional"
        )

    def test_producto_se_crea_correctamente(self):
        self.assertEqual(self.producto.nombre, "Balón Test")
        self.assertEqual(self.producto.precio, 22000)
        self.assertEqual(self.producto.stock, 10)

    def test_producto_str(self):
        self.assertEqual(str(self.producto), "Balón Test")

    def test_producto_descripcion_opcional(self):
        p = Producto.objects.create(nombre="Sin desc", precio=10000, stock=5, categoria="General")
        self.assertIsNone(p.descripcion)


class ProductoViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="Admin123!"
        )
        self.empleado = User.objects.create_user(
            username="empleado", email="empleado@test.com",
            password="Empleado123!", is_staff=True
        )
        self.cliente = User.objects.create_user(
            username="cliente", email="cliente@test.com", password="Cliente123!"
        )
        self.producto = Producto.objects.create(
            nombre="Guayos Test", precio=220000, stock=5,
            categoria="Calzado", descripcion="Guayos para césped"
        )

    def test_lista_productos_admin_puede_acceder(self):
        self.client.login(username="admin", password="Admin123!")
        response = self.client.get(reverse("productos:lista_productos"))
        self.assertEqual(response.status_code, 200)

    def test_lista_productos_empleado_puede_acceder(self):
        self.client.login(username="empleado", password="Empleado123!")
        response = self.client.get(reverse("productos:lista_productos"))
        self.assertEqual(response.status_code, 200)

    def test_lista_productos_cliente_redirigido(self):
        self.client.login(username="cliente", password="Cliente123!")
        response = self.client.get(reverse("productos:lista_productos"))
        self.assertEqual(response.status_code, 302)

    def test_crear_producto_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("productos:crear_producto"), {
            "nombre": "Uniforme Nuevo", "precio": "85000",
            "stock": "20", "categoria": "Ropa", "descripcion": "Uniforme deportivo"
        })
        self.assertEqual(Producto.objects.filter(nombre="Uniforme Nuevo").count(), 1)

    def test_crear_producto_cliente_denegado(self):
        self.client.login(username="cliente", password="Cliente123!")
        self.client.post(reverse("productos:crear_producto"), {
            "nombre": "Producto Intruso", "precio": "10000",
            "stock": "1", "categoria": "Otro"
        })
        self.assertEqual(Producto.objects.filter(nombre="Producto Intruso").count(), 0)

    def test_editar_producto_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("productos:editar_producto", args=[self.producto.id]), {
            "nombre": "Guayos Editados", "precio": "230000",
            "stock": "8", "categoria": "Calzado", "descripcion": "Actualizado"
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Guayos Editados")

    def test_eliminar_producto_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("productos:eliminar_producto", args=[self.producto.id]))
        self.assertEqual(Producto.objects.filter(id=self.producto.id).count(), 0)

    def test_eliminar_producto_cliente_denegado(self):
        self.client.login(username="cliente", password="Cliente123!")
        self.client.post(reverse("productos:eliminar_producto", args=[self.producto.id]))
        self.assertEqual(Producto.objects.filter(id=self.producto.id).count(), 1)