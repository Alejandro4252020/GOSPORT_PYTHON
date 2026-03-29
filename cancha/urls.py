from django.urls import path
from .views import lista_canchas, crear_cancha, eliminar_cancha
from . import views

urlpatterns = [
    path('', lista_canchas, name='lista_canchas'),
    path('crear/', crear_cancha, name='crear_cancha'),
    path('eliminar/<int:id>/', eliminar_cancha, name='eliminar_cancha'),
    path('editar/<int:id>/', views.editar_cancha, name='editar_cancha'),
]