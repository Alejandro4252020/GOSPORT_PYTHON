from django.contrib import admin
from django.urls import path
from . import views

#  IMPORTANTE
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('canchas/', views.canchas, name='canchas'),

    #  ESTA FALTABA
    path('canchas/<int:id>/', views.cancha_detalle, name='cancha_detalle'),

    path('catalogo/', views.catalogo, name='catalogo'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar', views.editar_perfil, name='editar_perfil'),
    path('carrito/', views.carrito, name='carrito'),
    path('productos/<int:id>/', views.producto_detalle, name='producto_detalle'),
]
#  ESTO HACE QUE LAS IMÁGENES FUNCIONEN
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)