# -*- coding: utf-8 -*-
"""
API serializer classes for notifications
"""

from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Common serializer for post
    """
    target_image = serializers.SerializerMethodField('_get_target_image_url')
    actor_image = serializers.SerializerMethodField('_get_actor_image_url')

    class Meta:
        model = Notification
        fields = ('id', 'unread', 'verb', 'description', 'timestamp','timesince', 'target_image', 'actor_image','type','badge')
        read_only_fields = ('id', 'verb', 'description', 'timestamp', 'timesince', 'target_image', 'actor_image')

    def _get_target_image_url(self, notification):
        """
        Get image as per the action for notification
        :param notification:  notification instance
        :return: image
        """
        try:
            image = notification.target.image
            if image:
                return self.context['request'].build_absolute_uri(image.medium.url)
        except Exception:
            return None

    def _get_actor_image_url(self, notification):
        """
        Get actor image.
        :param notification:
        :return: actor image
        """
        try:
            actor_image = notification.actor.image
            if actor_image:
                return self.context['request'].build_absolute_uri(actor_image.medium.url)
        except Exception:
            return None