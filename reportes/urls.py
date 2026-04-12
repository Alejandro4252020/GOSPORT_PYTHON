from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # REPORTE DE RESERVAS
    path('reservas/', views.reporte_reservas, name='reporte_reservas'),

    # EXPORTACIONES
    path('pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('excel/', views.exportar_excel, name='exportar_excel'),
    path('txt/', views.exportar_txt, name='exportar_txt'),
]