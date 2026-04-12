from django.db import models

class Usuario(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    )

    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')