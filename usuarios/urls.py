from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [

    # LISTAR
    path('', views.lista_usuarios, name='lista_usuarios'),

    # CREAR
    path('crear/', views.crear_usuario, name='crear_usuario'),

    # EDITAR
    path('editar/<int:id>/', views.editar_usuario, name='editar_usuario'),

    # ELIMINAR
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # EXPORTACIONES
    path('pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('excel/', views.exportar_excel, name='exportar_excel'),
    path('txt/', views.exportar_txt, name='exportar_txt'),

    # REPORTE
    path('reservas/', views.reporte_reservas, name='reporte_reservas'),
]