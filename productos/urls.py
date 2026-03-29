from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos),
    path('crear/', views.crear_producto),
    path('editar/<int:id>/', views.editar_producto),
    path('eliminar/<int:id>/', views.eliminar_producto),
]