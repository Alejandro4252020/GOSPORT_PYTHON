from django.db import models
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    stock = models.IntegerField()
    categoria = models.CharField(max_length=100, default='General')
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    activo = models.BooleanField(default=True)  # 👈 nuevo

    def __str__(self):
        return self.nombre