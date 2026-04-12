from django.urls import path
from . import views

app_name = 'canchas'  # 🔥 ESTO ES CLAVE

urlpatterns = [
    path('', views.lista_canchas, name='lista_canchas'),
    path('crear/', views.crear_cancha, name='crear_cancha'),
    path('editar/<int:id>/', views.editar_cancha, name='editar_cancha'),
    path('eliminar/<int:id>/', views.eliminar_cancha, name='eliminar_cancha'),
]