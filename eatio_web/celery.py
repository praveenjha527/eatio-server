from __future__ import absolute_import

import os


from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eatio_web.settings')

RABBIT_MQ = "amqp://guest:guest@ec2-54-77-251-47.eu-west-1.compute.amazonaws.com:5672//"

#REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

app = Celery('eatio', broker=RABBIT_MQ,)




# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
   CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
   BROKER_POOL_LIMIT = 1,
)

