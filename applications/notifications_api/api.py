# -*- coding: utf-8 -*-
"""
API view for notification
"""
from rest_framework import viewsets
from notifications.models import Notification

from common import mixins
from applications.notifications_api import serializers
from applications.accounts.models import User


class NotificationViewSet(mixins.UserRequired, viewsets.ModelViewSet):
    """
    List notification.
    """
    http_method_names = ['get', 'put']
    serializer_class = serializers.NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.id)
        return user.notifications.all()
