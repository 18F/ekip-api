import dj_database_url
import os
import tempfile
from .base import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '.everykidinapark.gov', # Allow domain and subdomains
    'kids-prod.18f.gov', # Internal URL for production instance 
    'kids.18f.gov', # Allow staging URL
    'kids-dev.18f.gov' # Allow development URL
    ]

DATABASES = {}
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['CONN_MAX_AGE'] = 60

AWS_STORAGE_BUCKET_NAME = os.getenv('EKIP_STATIC_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.getenv('EKIP_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('EKIP_AWS_SECRET_ACCESS_KEY')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.getenv('TMPDIR', tempfile.gettempdir()),
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
    }
}


# Don't add complex authentication related query parameters for requests
AWS_QUERYSTRING_AUTH = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
     'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

try:
  from .local_settings import *
except ImportError:
  pass
