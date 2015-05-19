from __future__ import absolute_import
from datetime import timedelta

from celery.task import PeriodicTask
from .weightage import execute_calculation
import logging


class SendEmailTask(PeriodicTask):
    """
    A periodic task that send email notification.
    # this will run every 60 seconds
    # send all emails in the mailer queue
    """
    run_every = timedelta(minutes=35)

    def run(self, **kwargs):
        execute_calculation()
        logging.info("calculate restaurant Weightage ")
        return True