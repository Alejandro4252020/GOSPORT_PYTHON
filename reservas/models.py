from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cancha_nombre = models.CharField(max_length=200)
    fecha = models.CharField(max_length=30)
    horario = models.CharField(max_length=30)
    personas = models.IntegerField(default=1)
    horas = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    imagen = models.CharField(max_length=200, blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cancha_nombre} - {self.fecha} ({self.usuario})"


class Compra(models.Model):
    factura = models.CharField(max_length=20, unique=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.factura:
            self.factura = f"GS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.factura} — {self.usuario.username}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto_nombre = models.CharField(max_length=200)
    producto_imagen = models.CharField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.producto_nombre} x{self.cantidad}"


# Signal para crear perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)