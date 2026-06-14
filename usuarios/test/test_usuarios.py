from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from usuarios.models import Usuario


class UsuarioModelTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            username="cliente1", email="cliente1@test.com",
            password="hashed_pass", rol="cliente"
        )

    def test_usuario_se_crea_correctamente(self):
        self.assertEqual(self.usuario.username, "cliente1")
        self.assertEqual(self.usuario.rol, "cliente")

    def test_usuario_roles_validos(self):
        roles = [r[0] for r in Usuario.ROLES]
        self.assertIn("admin", roles)
        self.assertIn("empleado", roles)
        self.assertIn("cliente", roles)

    def test_usuario_rol_por_defecto_es_cliente(self):
        u = Usuario.objects.create(username="nuevo", password="pass")
        self.assertEqual(u.rol, "cliente")


class UsuarioViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="Admin123!"
        )
        self.cliente = User.objects.create_user(
            username="cliente", email="cliente@test.com", password="Cliente123!"
        )
        self.usuario = Usuario.objects.create(
            username="usuario_crud", email="crud@test.com",
            password="pass", rol="cliente"
        )

    def test_lista_usuarios_admin_puede_acceder(self):
        self.client.login(username="admin", password="Admin123!")
        response = self.client.get(reverse("usuarios:lista_usuarios"))
        self.assertNotEqual(response.status_code, 500)

    def test_lista_usuarios_cliente_redirigido(self):
        self.client.login(username="cliente", password="Cliente123!")
        response = self.client.get(reverse("usuarios:lista_usuarios"))
        self.assertEqual(response.status_code, 302)

    def test_crear_usuario_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("usuarios:crear_usuario"), {
            "username": "nuevo_usuario", "email": "nuevo@test.com",
            "password": "Nuevo123!", "rol": "cliente"
        })
        self.assertEqual(Usuario.objects.filter(username="nuevo_usuario").count(), 1)

    def test_eliminar_usuario_admin_exitoso(self):
        self.client.login(username="admin", password="Admin123!")
        self.client.post(reverse("usuarios:eliminar_usuario", args=[self.usuario.id]))
        self.assertEqual(Usuario.objects.filter(id=self.usuario.id).count(), 0)

    def test_eliminar_usuario_cliente_denegado(self):
        self.client.login(username="cliente", password="Cliente123!")
        self.client.post(reverse("usuarios:eliminar_usuario", args=[self.usuario.id]))
        self.assertEqual(Usuario.objects.filter(id=self.usuario.id).count(), 1)