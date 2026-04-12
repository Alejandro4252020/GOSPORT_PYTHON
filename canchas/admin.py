from django.contrib import admin
from .models import Cancha

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'precio', 'capacidad', 'estado', 'direccion')
    list_filter = ('estado', 'tipo')
    search_fields = ('nombre', 'direccion')
