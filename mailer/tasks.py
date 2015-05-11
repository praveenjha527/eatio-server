from __future__ import absolute_import
from datetime import timedelta

from celery.task import PeriodicTask
from mailer.engine import send_all


class SendEmailTask(PeriodicTask):
    """
    A periodic task that send email notification.
    # this will run every 30 seconds
    # send all emails in the mailer queue
    """
    run_every = timedelta(seconds=30)

    def run(self, **kwargs):
        print "sending email"
        send_all()
        return True