import dj_database_url
import os

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {}
DATABASES['default'] = dj_database_url.config()

AWS_STORAGE_BUCKET_NAME = os.getenv('EKIP_STATIC_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.getenv('EKIP_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('EKIP_AWS_SECRET_ACCESS_KEY')


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

try:
  from .local_settings import *
except ImportError:
  pass
