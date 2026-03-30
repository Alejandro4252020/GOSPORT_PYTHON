from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # CANCHAS
    path('canchas/', views.canchas, name='canchas'),
    path('canchas/<int:id>/', views.cancha_detalle, name='cancha_detalle'),

    # ✅ RESERVAR (NUEVO)
    path('reservar/<int:id>/', views.reservar, name='reservar'),

    # OTROS
    path('catalogo/', views.catalogo, name='catalogo'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar', views.editar_perfil, name='editar_perfil'),
    path('carrito/', views.carrito, name='carrito'),
    path('productos/<int:id>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/eliminar/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
]

# IMÁGENES MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)