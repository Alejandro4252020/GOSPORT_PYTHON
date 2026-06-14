from .settings import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',  # noqa: F405
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
        'level': 'CRITICAL',
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
    },
}

# Monkey-patch para Python 3.14 + Django incompatibility
# El __copy__ de BaseContext falla porque super().__copy__() no funciona en Python 3.14
import django.template.context as _ctx
import copy as _copy

def _base_context_copy(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__.update(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate

def _request_context_copy(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__.update(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate

_ctx.BaseContext.__copy__ = _base_context_copy
_ctx.Context.__copy__ = _base_context_copy
_ctx.RequestContext.__copy__ = _request_context_copy

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'