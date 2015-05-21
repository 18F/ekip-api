import dj_database_url

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {}
DATABASES['default'] = dj_database_url.config()

try:
  from .local_settings import *
except ImportError:
  pass