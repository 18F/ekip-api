from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'ekip',                      
        'USER': 'ekip',
        'PASSWORD': 'ekip',
        'HOST': 'localhost',
        'PORT': '',
    }
}

INTERNAL_IPS = ['127.0.0.1', '::1', '192.168.19.16']

CACHES = {
    'default': { 
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

try:
  from .local_settings import *
except ImportError:
  pass
