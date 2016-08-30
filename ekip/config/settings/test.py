from .base import *

#Do not include the LoginRequiredMiddleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

CACHES = {
    'default': { 
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

if 'TRAVIS' in os.environ:
    # Use Postgres.
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
else:
    # The test database can just be sqlite.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'ekip',
        }
    }