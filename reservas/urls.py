from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from . import views

urlpatterns = [

    # VISTAS PÚBLICAS
    path('', views.home, name='home'),
    path('home/', lambda request: redirect('reservas:home'), name='home_alias'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('canchas/', views.canchas_publico, name='canchas_publico'),
    path('canchas/<int:id>/', views.cancha_detalle, name='cancha_detalle'),
    path('cancha-db/<int:id>/', views.cancha_detalle_db, name='cancha_detalle_db'),
    path('productos/<int:id>/', views.producto_detalle, name='producto_detalle'),
    path('contacto/', views.contacto, name='contacto'),

    # LOGIN REQUIRED
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('perfil/', login_required(views.perfil), name='perfil'),
    path('perfil/editar/', login_required(views.editar_perfil), name='editar_perfil'),
    path('carrito/', login_required(views.carrito), name='carrito'),
    path('carrito/eliminar/', login_required(views.eliminar_del_carrito), name='eliminar_del_carrito'),
    path('carrito/vaciar/', login_required(views.vaciar_carrito), name='vaciar_carrito'),
    path('comprar/', login_required(views.comprar), name='comprar'),
    path('factura/<int:compra_id>/', login_required(views.factura), name='factura'),

    # RESERVAS
    path('reservar/<int:id>/', login_required(views.reservar), name='reservar'),
    path('reservar-db/<int:id>/', login_required(views.reservar_db), name='reservar_db'),
    path('confirmacion/', login_required(views.confirmacion_reserva), name='confirmacion_reserva'),
    path('reserva/<int:id>/', login_required(views.ver_reserva), name='ver_reserva'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)