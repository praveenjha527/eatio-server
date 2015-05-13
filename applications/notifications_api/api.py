# -*- coding: utf-8 -*-
"""
API view for notification
"""
from push_notifications.models import GCMDevice
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
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


class RegisterAndroidDeviceTokenViewSet(APIView , mixins.UserRequired):
    """
    @inputparams:
    {
      "registration_id": "registration_id"
    }
    """
    model = GCMDevice

    def post(self,request):
        """
        Set the object's user, based on the incoming request.
        """
        device, created = self.model.objects.get_or_create(user=request.user)
        try:
            device.name = request.user.first_name
            device.registration_id = request.DATA['registration_id']
            device.save()
            return Response({'status': 'success'})
        except Exception, e:
            return Response({'error': str(e)})
