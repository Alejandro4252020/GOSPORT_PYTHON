from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('reservas.urls')),  # HOME PRINCIPAL

    # 🔥 CORRECCIÓN AQUÍ
    path('auth/', include(('login_register.urls', 'auth'), namespace='auth')),
]