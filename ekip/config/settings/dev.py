from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ekip',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'ekip',
        'PASSWORD': 'ekip',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

INTERNAL_IPS = ['127.0.0.1', '::1', '192.168.19.16']

try:
  from .local_settings import *
except ImportError:
  pass
