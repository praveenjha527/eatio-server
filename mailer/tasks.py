from __future__ import absolute_import
from datetime import timedelta

from celery.task import PeriodicTask, task
from mailer.engine import send_all


@task()
def send_queued_emails(*args, **kwargs):
    send_all()
