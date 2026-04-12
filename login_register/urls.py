from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    # 🔥 LOGOUT CORREGIDO (SIN 405)
    path('logout/', auth_views.LogoutView.as_view(next_page='auth:login'), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
]