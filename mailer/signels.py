# coding=utf-8
# pylint: disable=unused-argument
"""
Hook custom signals here.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from mailer.models import Message
from notifications.tasks import send_mails_all


@receiver(post_save, sender=Message)
def invalidate_glossary(sender, instance, **kwargs):
    send_mails_all.delay()