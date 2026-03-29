from django.urls import path
from .views import lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario
from . import views

urlpatterns = [
    path('', lista_usuarios, name='lista_usuarios'),
    path('crear/', crear_usuario, name='crear_usuario'),
    path('editar/<int:id>/', editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    # Exportar
    path('pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('excel/', views.exportar_excel, name='exportar_excel'),
    path('txt/', views.exportar_txt, name='exportar_txt'),
]