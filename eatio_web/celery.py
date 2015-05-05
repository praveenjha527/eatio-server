from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eatio_web.settings')


app = Celery('eatio_web', backend='amqp')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
   CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
   BROKER_POOL_LIMIT = 1,
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))