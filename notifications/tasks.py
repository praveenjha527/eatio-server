from __future__ import absolute_import


from celery import shared_task



@shared_task
def send_push_notification(notification):
    """
    Sends push notification in background and returns True if it could be sent, else false

    """
    print "sending notification"
    print notification
    return notification.send_push_notification()

