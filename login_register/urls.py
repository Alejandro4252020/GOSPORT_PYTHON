from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # URL raíz para login
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]