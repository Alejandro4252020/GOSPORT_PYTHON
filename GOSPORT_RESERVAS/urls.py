from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static
from reservas import views as reservas_views


# ✅ HOME → REDIRIGE AL HOME REAL SI ESTÁ LOGUEADO, AL LOGIN SI NO
def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('reservas:home'))
    return redirect(reverse('auth:login'))


urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ ENTRADA PRINCIPAL → HOME O LOGIN
    path('', home, name='home'),

    # ✅ /home/ → MISMA LÓGICA
    path('home/', home, name='home_redirect'),

    # ✅ LOGIN DIRECTO
    path('login/', lambda request: redirect(reverse('auth:login'))),

    # =========================
    # APPS
    # =========================

    path('reservas/', include(('reservas.urls', 'reservas'), namespace='reservas')),
    path('auth/', include(('login_register.urls', 'auth'), namespace='auth')),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('productos/', include(('productos.urls', 'productos'), namespace='productos')),
    path('canchas/', include(('canchas.urls', 'canchas'), namespace='canchas')),
    path('reportes/', include(('reportes.urls', 'reportes'), namespace='reportes')),

    # 🔥 RUTA DIRECTA OPCIONAL (/reservar/1/)
    path('reservar/<int:id>/', reservas_views.reservar, name='reservar_directo'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)