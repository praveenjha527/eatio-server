from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eatio_db',
        'USER': 'sayone_eatio',
        'PASSWORD': 'B8hzA8eG',
        'HOST': 'eatio.cofer1yssdmz.ap-southeast-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']


INSTALLED_APPS+= (
    'djcelery',
)

import djcelery
djcelery.setup_loader()