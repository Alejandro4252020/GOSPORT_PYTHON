from django.db import models

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    rol = models.CharField(max_length=20)
    password = models.CharField(max_length=255)  # 🔐 NUEVO

    def __str__(self):
        return self.username