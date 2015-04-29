from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file':
                '/home/sayonetech/webapps/eatio_production/eatio_web/eatio_web/db_files/my_production.cnf',
            'init_command': 'SET storage_engine=INNODB',
        },
    }
}