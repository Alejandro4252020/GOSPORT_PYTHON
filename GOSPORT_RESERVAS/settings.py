"""
Django settings for GOSPORT_RESERVAS project.
"""

import os
from pathlib import Path

import pymysql
import environ

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# VARIABLES DE ENTORNO
# =====================================================

env = environ.Env()

env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-change-this-in-production"
)

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["*"]
)

# =====================================================
# APLICACIONES
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'login_register',
    'reservas',
    'usuarios',
    'productos',
    'reportes',
    'canchas',
]

# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =====================================================
# URLS Y WSGI
# =====================================================

ROOT_URLCONF = 'GOSPORT_RESERVAS.urls'

WSGI_APPLICATION = 'GOSPORT_RESERVAS.wsgi.application'

# =====================================================
# TEMPLATES
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =====================================================
# BASE DE DATOS MYSQL (RAILWAY)
# =====================================================

DATABASES = {
    'default': {
        'ENGINE': env(
            'DB_ENGINE',
            default='django.db.backends.mysql'
        ),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# =====================================================
# CACHÉ EN MEMORIA (mejora rendimiento bajo carga)
# =====================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "gosport-cache",
    }
}

# =====================================================
# VALIDADORES DE CONTRASEÑA
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# =====================================================
# INTERNACIONALIZACIÓN
# =====================================================

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

# =====================================================
# ARCHIVOS ESTÁTICOS
# =====================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# =====================================================
# MEDIA
# =====================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# =====================================================
# AUTENTICACIÓN
# =====================================================

LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = '/reservas/'

LOGOUT_REDIRECT_URL = '/auth/login/'

# =====================================================
# CSRF
# =====================================================

CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://*.up.railway.app",
    "https://modulator-slit-frolic.ngrok-free.dev",
    "https://*.ngrok-free.app",
    "https://*.ngrok-free.dev",
]

# =====================================================
# MODELOS
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'