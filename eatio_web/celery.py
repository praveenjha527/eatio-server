from __future__ import absolute_import

import os


from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eatio_web.settings')

RABBIT_MQ = "amqp://eatio:pwdeatio@localhost:5672/eatio_host/"

#REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

app = Celery('eatio', backend='amqp',broker=RABBIT_MQ)



# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
   CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
   BROKER_POOL_LIMIT = 1,
)

