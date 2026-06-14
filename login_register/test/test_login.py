from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginRegisterTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="Test123!"
        )

    def test_login_correcto(self):
        response = self.client.post(reverse("auth:login"), {
            "email": "test@test.com", "password": "Test123!"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_password_incorrecto(self):
        response = self.client.post(reverse("auth:login"), {
            "email": "test@test.com", "password": "Wrongpass1!"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_email_no_existe(self):
        response = self.client.post(reverse("auth:login"), {
            "email": "noexiste@test.com", "password": "Test123!"
        })
        self.assertEqual(response.status_code, 200)

    def test_registro_exitoso(self):
        self.client.post(reverse("auth:register"), {
            "username": "nuevo", "email": "nuevo@test.com",
            "password": "Nuevo123!", "password2": "Nuevo123!"
        })
        self.assertEqual(User.objects.filter(username="nuevo").count(), 1)

    def test_registro_passwords_no_coinciden(self):
        self.client.post(reverse("auth:register"), {
            "username": "otro", "email": "otro@test.com",
            "password": "Otro123!", "password2": "Diferente123!"
        })
        self.assertEqual(User.objects.filter(username="otro").count(), 0)

    def test_registro_usuario_duplicado(self):
        self.client.post(reverse("auth:register"), {
            "username": "testuser", "email": "otro2@test.com",
            "password": "Test123!", "password2": "Test123!"
        })
        self.assertEqual(User.objects.filter(username="testuser").count(), 1)

    def test_registro_password_corta(self):
        self.client.post(reverse("auth:register"), {
            "username": "corto", "email": "corto@test.com",
            "password": "abc", "password2": "abc"
        })
        self.assertEqual(User.objects.filter(username="corto").count(), 0)

    def test_logout_redirige(self):
        self.client.login(username="testuser", password="Test123!")
        response = self.client.get(reverse("auth:logout"))
        self.assertEqual(response.status_code, 302)