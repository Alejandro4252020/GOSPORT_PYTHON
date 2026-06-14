import io
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from canchas.models import Cancha


def crear_imagen_test(nombre="test.jpg"):
    img = Image.new('RGB', (100, 100), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(nombre, buffer.read(), content_type="image/jpeg")


class CanchaModelTest(TestCase):

    def setUp(self):
        self.cancha = Cancha.objects.create(
            nombre="Cancha Test",
            tipo="Futsal",
            precio=50000,
            capacidad=10,
            estado="disponible",
            direccion="Calle 123, Bogotá",
            imagen=""
        )

    def test_cancha_se_crea_correctamente(self):
        self.assertEqual(self.cancha.nombre, "Cancha Test")
        self.assertEqual(float(self.cancha.precio), 50000)
        self.assertEqual(self.cancha.estado, "disponible")

    def test_cancha_str(self):
        self.assertEqual(str(self.cancha), "Cancha Test")

    def test_cancha_estados_validos(self):
        estados = [e[0] for e in Cancha.ESTADOS]
        self.assertIn("disponible", estados)
        self.assertIn("ocupado", estados)
        self.assertIn("mantenimiento", estados)


class CanchaViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="Admin123!"
        )
        self.cliente = User.objects.create_user(
            username="cliente", email="cliente@test.com", password="Cliente123!"
        )
        self.cancha = Cancha.objects.create(
            nombre="Cancha Test", tipo="Futsal", precio=50000,
            capacidad=10, estado="disponible", direccion="Calle 123", imagen=""
        )

    def test_lista_canchas_admin_puede_acceder(self):
        self.client.login(username="admin", password="Admin123!")
        response = self.client.get(reverse("canchas:lista_canchas"))
        self.assertEqual(response.status_code, 200)

    def test_lista_canchas_cliente_redirigido(self):
        self.client.login(username="cliente", password="Cliente123!")
        response = self.client.get(reverse("canchas:lista_canchas"))
        self.assertEqual(response.status_code, 302)

    def test_lista_canchas_sin_login_redirige(self):
        response = self.client.get(reverse("canchas:lista_canchas"))
        self.assertEqual(response.status_code, 302)

    def test_crear_cancha_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("canchas:crear_cancha"), {
            "nombre": "Cancha Nueva", "tipo": "Fútbol", "precio": "60000",
            "capacidad": "12", "estado": "disponible", "direccion": "Av. Principal 456",
            "imagen": crear_imagen_test("test.jpg"),
        })
        self.assertEqual(Cancha.objects.filter(nombre="Cancha Nueva").count(), 1)

    def test_crear_cancha_cliente_denegado(self):
        self.client.login(username="cliente", password="Cliente123!")
        self.client.post(reverse("canchas:crear_cancha"), {
            "nombre": "Cancha Intruso", "tipo": "Fútbol", "precio": "60000",
            "capacidad": "12", "estado": "disponible", "direccion": "Calle Falsa",
        })
        self.assertEqual(Cancha.objects.filter(nombre="Cancha Intruso").count(), 0)

    def test_editar_cancha_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("canchas:editar_cancha", args=[self.cancha.id]), {
            "nombre": "Cancha Editada", "tipo": "Futsal", "precio": "55000",
            "capacidad": "10", "estado": "ocupado", "direccion": "Nueva Dirección",
            "imagen": crear_imagen_test("test2.jpg"),
        })
        self.cancha.refresh_from_db()
        self.assertEqual(self.cancha.nombre, "Cancha Editada")

    def test_eliminar_cancha_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("canchas:eliminar_cancha", args=[self.cancha.id]))
        self.assertEqual(Cancha.objects.filter(id=self.cancha.id).count(), 0)

    def test_eliminar_cancha_cliente_denegado(self):
        self.client.login(username="cliente", password="Cliente123!")
        self.client.post(reverse("canchas:eliminar_cancha", args=[self.cancha.id]))
        self.assertEqual(Cancha.objects.filter(id=self.cancha.id).count(), 1)