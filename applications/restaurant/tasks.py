from __future__ import absolute_import
from datetime import timedelta

from celery.task import PeriodicTask
from .weightage import execute_calculation
import logging


class RunCalculationPeriodically(PeriodicTask):
    """
    A periodic task that calculate weightage of restaurants.
    # this will run every 35 seconds
    """
    run_every = timedelta(minutes=35)

    def run(self, **kwargs):
        execute_calculation()
        logging.info("calculate restaurant Weightage ")
        return True