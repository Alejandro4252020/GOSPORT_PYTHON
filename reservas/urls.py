from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [

    # Vistas públicas
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('canchas/', views.canchas, name='canchas'),
    path('canchas/<int:id>/', views.cancha_detalle, name='cancha_detalle'),
    path('productos/<int:id>/', views.producto_detalle, name='producto_detalle'),
    path('contacto/', views.contacto, name='contacto'),

    # Login required
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('perfil/', login_required(views.perfil), name='perfil'),
    path('perfil/editar', login_required(views.editar_perfil), name='editar_perfil'),
    path('carrito/', login_required(views.carrito), name='carrito'),
    path('carrito/eliminar/', login_required(views.eliminar_del_carrito), name='eliminar_del_carrito'),
    path('carrito/vaciar/', login_required(views.vaciar_carrito), name='vaciar_carrito'),

    # Reservas
    path('reservar/<int:id>/', login_required(views.reservar), name='reservar'),
    path('confirmacion/', login_required(views.confirmacion_reserva), name='confirmacion_reserva'),
    path('reserva/<int:id>/', login_required(views.ver_reserva), name='ver_reserva'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)