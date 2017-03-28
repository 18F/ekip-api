from cfenv import AppEnv
import dj_database_url
import os
import re
import tempfile
from .base import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '.everykidinapark.gov', # Allow domain and subdomains
    'kids-prod.18f.gov', 'ekip-prod.app.cloud.gov', # Internal URL for production instance
    'kids.18f.gov', 'ekip-staging.app.cloud.gov', # Allow staging URL
    'kids-dev.18f.gov', 'ekip-dev.app.cloud.gov' # Allow development URL
    ]

database_url = os.getenv('DATABASE_URL')
env = AppEnv()
cf_db = env.get_service(name=re.compile('ekip-db'))
if cf_db:
    database_url = cf_db.credentials['uri']
DATABASES = {}
DATABASES['default'] = dj_database_url.parse(database_url)
DATABASES['default']['CONN_MAX_AGE'] = 60

AWS_S3_REGION_NAME = os.getenv('EKIP_AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('EKIP_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('EKIP_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('EKIP_STATIC_BUCKET_NAME')
cf_s3 = env.get_service(name=re.compile('ekip-s3'))
if cf_s3:
    AWS_STORAGE_BUCKET_NAME = cf_s3.credentials['bucket']
    AWS_S3_REGION_NAME = cf_s3.credentials['region']
    AWS_ACCESS_KEY_ID = cf_s3.credentials['access_key_id']
    AWS_SECRET_ACCESS_KEY = cf_s3.credentials['secret_access_key']
AWS_S3_CUSTOM_DOMAIN = 's3-%s.amazonaws.com/%s' % (AWS_S3_REGION_NAME, AWS_STORAGE_BUCKET_NAME)
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Allow secret key to be retreieved from UPS if on Cloud Foundry
ekip_creds = env.get_service(name='ekip-django')
if ekip_creds is not None:
    SECRET_KEY = ekip_creds.credentials['DJANGO_SECRET_KEY']

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
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CORS_ORIGIN_ALLOW_ALL = True

try:
  from .local_settings import *
except ImportError:
  pass
