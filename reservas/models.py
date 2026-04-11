from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username


# 👇 MODELOS AGREGADOS (NO AFECTAN LO EXISTENTE)

class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    imagen = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    imagen = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# 👇 SIGNAL MEJORADO (evita duplicados)
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)