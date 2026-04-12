from django.db import models

class Cancha(models.Model):

    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    direccion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='canchas/')

    def __str__(self):
        return self.nombre