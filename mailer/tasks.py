from __future__ import absolute_import
from datetime import timedelta

from celery.task import PeriodicTask
from mailer.engine import send_all 
import logging


class SendEmailTask(PeriodicTask):
    """
    A periodic task that send email notification.
    # this will run every 60 seconds
    # send all emails in the mailer queue
    """
    run_every = timedelta(seconds=3000)

    def run(self, **kwargs):
        send_all()
        logging.info("sending email running fine, without errors.")
        return True