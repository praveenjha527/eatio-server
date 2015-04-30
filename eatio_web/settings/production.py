from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eatio_db',
        'USER': 'sayone_eatio',
        'PASSWORD': 'B8hzA8eG',
        'HOST': '',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']