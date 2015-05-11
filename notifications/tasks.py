from __future__ import absolute_import

from celery import shared_task, task

from mailer.engine import send_all


@shared_task
def send_push_notification(notification):
    """
    Sends push notification in background and returns True if it could be sent, else false

    """
    print "sending notification"
    return notification.send_push_notification()


@task
def send_mails_all():
    send_all()
    return True
