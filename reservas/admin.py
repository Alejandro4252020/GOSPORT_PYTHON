from django.contrib import admin
from .models import Perfil, Reserva

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'cancha_nombre', 'fecha', 'horario', 'personas', 'horas', 'total', 'creada')
    list_filter = ('fecha', 'cancha_nombre')
    search_fields = ('cancha_nombre', 'usuario__username')
