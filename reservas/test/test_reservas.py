from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from reservas.models import Reserva, Compra, DetalleCompra, Perfil
from canchas.models import Cancha


class ReservaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario_test", email="user@test.com", password="User123!"
        )
        self.reserva = Reserva.objects.create(
            usuario=self.user, cancha_nombre="Cancha Test",
            fecha="15/06/2025", horario="08:00 AM",
            personas=5, horas=2, total=100000, imagen="cancha.jpg"
        )

    def test_reserva_se_crea_correctamente(self):
        self.assertEqual(self.reserva.cancha_nombre, "Cancha Test")
        self.assertEqual(self.reserva.personas, 5)
        self.assertEqual(self.reserva.total, 100000)

    def test_reserva_str(self):
        esperado = f"Cancha Test - 15/06/2025 ({self.user})"
        self.assertEqual(str(self.reserva), esperado)

    def test_reserva_sin_usuario(self):
        reserva = Reserva.objects.create(
            usuario=None, cancha_nombre="Cancha Invitado",
            fecha="20/06/2025", horario="10:00 AM",
            personas=3, horas=1, total=50000
        )
        self.assertIsNone(reserva.usuario)


class CompraModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="comprador", email="comprador@test.com", password="Compra123!"
        )
        self.compra = Compra.objects.create(usuario=self.user, total=150000)

    def test_compra_factura_generada_automaticamente(self):
        self.assertTrue(self.compra.factura.startswith("GS-"))

    def test_compra_factura_unica(self):
        compra2 = Compra.objects.create(usuario=self.user, total=50000)
        self.assertNotEqual(self.compra.factura, compra2.factura)

    def test_detalle_compra_subtotal(self):
        detalle = DetalleCompra.objects.create(
            compra=self.compra, producto_nombre="Balón", precio=22000, cantidad=3
        )
        self.assertEqual(detalle.subtotal, 66000)

    # ✅ NUEVO — verifica que bulk_create inserta todos los detalles correctamente
    def test_detalle_compra_bulk_create(self):
        detalles = [
            DetalleCompra(
                compra=self.compra, producto_nombre="Balón",
                producto_imagen="", precio=22000, cantidad=2
            ),
            DetalleCompra(
                compra=self.compra, producto_nombre="Guayos",
                producto_imagen="", precio=220000, cantidad=1
            ),
            DetalleCompra(
                compra=self.compra, producto_nombre="Uniforme",
                producto_imagen="", precio=85000, cantidad=3
            ),
        ]
        DetalleCompra.objects.bulk_create(detalles)
        self.assertEqual(DetalleCompra.objects.filter(compra=self.compra).count(), 3)

    # ✅ NUEVO — verifica que bulk_create calcula subtotales correctamente
    def test_detalle_compra_bulk_create_subtotales(self):
        detalles = [
            DetalleCompra(
                compra=self.compra, producto_nombre="Balón",
                producto_imagen="", precio=22000, cantidad=2
            ),
            DetalleCompra(
                compra=self.compra, producto_nombre="Guayos",
                producto_imagen="", precio=220000, cantidad=1
            ),
        ]
        DetalleCompra.objects.bulk_create(detalles)
        total = sum(d.subtotal for d in DetalleCompra.objects.filter(compra=self.compra))
        self.assertEqual(total, 264000)


class PerfilModelTest(TestCase):

    def test_perfil_creado_automaticamente_con_usuario(self):
        user = User.objects.create_user(
            username="nuevo_user", email="nuevo@test.com", password="Nuevo123!"
        )
        self.assertTrue(Perfil.objects.filter(user=user).exists())

    def test_perfil_str(self):
        user = User.objects.create_user(username="perfil_user", password="Perfil123!")
        perfil = Perfil.objects.get(user=user)
        self.assertEqual(str(perfil), "perfil_user")


class ReservaViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="reservador", email="reservador@test.com", password="Reserva123!"
        )
        self.cancha = Cancha.objects.create(
            nombre="Cancha Vista Test", tipo="Futsal", precio=50000,
            capacidad=10, estado="disponible", direccion="Calle 1", imagen=""
        )

    def test_home_accesible_sin_login(self):
        response = self.client.get(reverse("reservas:home"))
        self.assertNotEqual(response.status_code, 500)

    def test_home_muestra_canchas_y_productos(self):
        response = self.client.get(reverse("reservas:home"))
        self.assertIn("canchas", response.context)
        self.assertIn("productos", response.context)

    # ✅ NUEVO — verifica que el caché de canchas funciona correctamente
    def test_home_canchas_provienen_de_cache(self):
        from django.core.cache import cache
        cache.clear()
        response = self.client.get(reverse("reservas:home"))
        self.assertIsNotNone(cache.get('canchas_db_all'))

    # ✅ NUEVO — verifica que el caché de productos funciona correctamente
    def test_home_productos_provienen_de_cache(self):
        from django.core.cache import cache
        cache.clear()
        response = self.client.get(reverse("reservas:home"))
        self.assertIsNotNone(cache.get('productos_db_all'))

    def test_contacto_get(self):
        response = self.client.get(reverse("reservas:contacto"))
        self.assertNotEqual(response.status_code, 500)

    def test_contacto_post_valido(self):
        response = self.client.post(reverse("reservas:contacto"), {
            "nombre": "Alejo", "correo": "alejo@test.com", "mensaje": "Hola"
        })
        self.assertEqual(response.status_code, 302)

    def test_carrito_get_vacio(self):
        self.client.login(username="reservador", password="Reserva123!")
        response = self.client.get(reverse("reservas:carrito"))
        self.assertNotEqual(response.status_code, 500)

    def test_agregar_producto_al_carrito(self):
        self.client.login(username="reservador", password="Reserva123!")
        self.client.post(reverse("reservas:carrito"), {
            "productoId": 1, "cantidad": 2, "source": "hardcoded"
        })
        carrito = self.client.session.get("carrito", [])
        self.assertEqual(len(carrito), 1)
        self.assertEqual(carrito[0]["cantidad"], 2)

    def test_vaciar_carrito(self):
        self.client.login(username="reservador", password="Reserva123!")
        session = self.client.session
        session["carrito"] = [{"id": 1, "nombre": "Balón", "precio": 22000, "cantidad": 1}]
        session.save()
        self.client.post(reverse("reservas:vaciar_carrito"))
        self.assertEqual(self.client.session.get("carrito"), [])

    def test_comprar_requiere_login(self):
        response = self.client.post(reverse("reservas:comprar"))
        self.assertEqual(response.status_code, 302)

    def test_comprar_exitoso(self):
        self.client.login(username="reservador", password="Reserva123!")
        session = self.client.session
        session["carrito"] = [{"id": 1, "nombre": "Balón", "precio": 22000, "imagen": "", "cantidad": 2}]
        session.save()
        self.client.post(reverse("reservas:comprar"))
        self.assertEqual(Compra.objects.filter(usuario=self.user).count(), 1)

    # ✅ NUEVO — verifica que bulk_create inserta los detalles al comprar
    def test_comprar_crea_detalles_con_bulk_create(self):
        self.client.login(username="reservador", password="Reserva123!")
        session = self.client.session
        session["carrito"] = [
            {"id": 1, "nombre": "Balón", "precio": 22000, "imagen": "", "cantidad": 2},
            {"id": 2, "nombre": "Guayos", "precio": 220000, "imagen": "", "cantidad": 1},
        ]
        session.save()
        self.client.post(reverse("reservas:comprar"))
        compra = Compra.objects.filter(usuario=self.user).first()
        self.assertEqual(DetalleCompra.objects.filter(compra=compra).count(), 2)

    def test_reservar_cancha_publica_get(self):
        self.client.login(username="reservador", password="Reserva123!")
        response = self.client.get(reverse("reservas:reservar", args=[self.cancha.id]))
        self.assertNotEqual(response.status_code, 500)

    def test_reservar_post_valido_crea_reserva(self):
        self.client.login(username="reservador", password="Reserva123!")
        self.client.post(reverse("reservas:reservar", args=[self.cancha.id]), {
            "dia": "20", "horas": "2", "personas": "5", "horario": "08:00 AM"
        })
        self.assertEqual(Reserva.objects.count(), 1)

    def test_reservar_personas_invalidas(self):
        self.client.login(username="reservador", password="Reserva123!")
        # 51 is invalid because MAX_PERSONAS is 50
        self.client.post(reverse("reservas:reservar", args=[self.cancha.id]), {
            "dia": "20", "horas": "2", "personas": "51", "horario": "08:00 AM"
        })
        self.assertEqual(Reserva.objects.count(), 0)

    def test_reservar_excede_tope_precio(self):
        self.client.login(username="reservador", password="Reserva123!")
        # Create a cancha with price 300,000
        cancha_cara = Cancha.objects.create(
            nombre="Cancha Cara", tipo="Futsal", precio=300000,
            capacidad=10, estado="disponible", direccion="Calle 2", imagen=""
        )
        # Reserving for 4 hours yields 1,200,000 COP, which exceeds 1,000,000 COP
        self.client.post(reverse("reservas:reservar_db", args=[cancha_cara.id]), {
            "dia": "20", "horas": "4", "personas": "5", "horario": "08:00 AM"
        })
        self.assertEqual(Reserva.objects.filter(cancha_nombre="Cancha Cara").count(), 0)

    def test_reservar_horas_invalidas(self):
        self.client.login(username="reservador", password="Reserva123!")
        self.client.post(reverse("reservas:reservar", args=[self.cancha.id]), {
            "dia": "20", "horas": "10", "personas": "5", "horario": "08:00 AM"
        })
        self.assertEqual(Reserva.objects.count(), 0)