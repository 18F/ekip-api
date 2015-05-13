from .base import *


# The test database can just be sqlite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ekip',
    }
}
