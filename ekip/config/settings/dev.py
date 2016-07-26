from .base import *

DEBUG = False

#  TEMPLATE_DEBUG = True
#  Replaced to remove TEMPLATE_* error message during manage.py check and manage.py runserver commands.
#  This is an exact duplicate of what is in base.py but appended with 'debug' in the 'OPTIONS' block.


ALLOWED_HOSTS = [
    '*'
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages', 
                'django.core.context_processors.request'],
            'debug': DEBUG
        }
    }
]

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


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

try:
  from .local_settings import *
except ImportError:
  pass
