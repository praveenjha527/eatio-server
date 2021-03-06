# -*- coding: utf-8 -*-
"""
API view for profile
"""
from allauth.socialaccount.models import SocialAccount
from django.core.files.base import ContentFile
from django.http import Http404
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from requests import request

from django.contrib.auth import login
from django.conf import settings

from applications.accounts import models as account_models
from applications.accounts.models import PasswordReset, HelpTicket, SignupCode
from applications.accounts.serializers import ResetPasswordSerializer, HelpTicketSerializer, ChangePasswordSerializer
from applications.utils.utils import get_admin, create_referral_code
from common import mixins
from common.mixins import UserRequired
from applications.accounts import serializers
from notifications.models import create_bonus_point_received_notification


class UserRegisterViewSet(viewsets.ModelViewSet):
    """
    View set for registration.
    :parameter     username
    :parameter     password
    :parameter     mobile or email
    """
    http_method_names = ['post', ]
    serializer_class = serializers.UserRegisterSerializer
    queryset = account_models.User.objects.all()

    def perform_create(self, serializer):
        from models import send_signup_email
        from eatio_web.settings import base as settings
        instance = serializer.save()

        send_signup_email(instance)
        #TODO Integration with mixpanel

        obj, created = SignupCode.objects.get_or_create(user=instance, code = create_referral_code(instance.username))

        if settings.GENERATE_SIGNUP_BONUS_AND_NOTIFY:
            create_bonus_point_received_notification(get_admin(),instance)


class ProfileEditViewSet(UserRequired, viewsets.ModelViewSet):
    """
    View set to update profile of current user.
    """
    http_method_names = ['put', 'get']
    serializer_class = serializers.UserSerializerWithReview
    queryset = account_models.User.objects.all()

    def update(self, request, *args, **kwargs):
        """
        Update method to check the url. to support edit
        """
        if self.kwargs.get('pk') != "edit":
            raise Http404
        return super(ProfileEditViewSet, self).update(request, *args, **kwargs)

    def get_object(self):
        """
        Get user object.
        """
        return account_models.User.objects.get(id=self.request.user.id)

    def get_queryset(self):
        if not self.kwargs.get('pk'):
            raise Http404
        return super(ProfileEditViewSet, self).get_queryset()


class SocialLoginBase(SocialLogin):

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, self.created = self.token_model.objects.get_or_create(
            user=self.user)

        if self.created:
            try:
                social_obj = SocialAccount.objects.get(user=self.user)
                self.user.name = social_obj.extra_data[u'name']
                self.user.gender = social_obj.extra_data[u'gender']
                if u'email' in social_obj.extra_data:
                    self.user.email = social_obj.extra_data[u'email']
                self.user.save()
                url = 'http://graph.facebook.com/{0}/picture?type=large'.format(social_obj.extra_data[u'id'])
                response = request('GET', url, params={'type': 'large'})
                response.raise_for_status()
                self.user.image.save('{0}_social.jpg'.format(social_obj.extra_data[u'name']),
                                   ContentFile(response.content))
            except Exception:
                pass
        from models import send_signup_email
        from eatio_web.settings import base as settings
        try:
            if self.created:
                send_signup_email(self.user)
        except Exception:
            pass
        #TODO Integration with mixpanel

        if self.created:
            obj, created = SignupCode.objects.get_or_create(user=self.user, code = create_referral_code(self.user.username))

        if settings.GENERATE_SIGNUP_BONUS_AND_NOTIFY and self.created:
            create_bonus_point_received_notification(get_admin(),self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response({'token': self.token.key, 'already_connected': not self.created, }, status=status.HTTP_200_OK)


class FacebookLogin(SocialLoginBase):
    adapter_class = FacebookOAuth2Adapter


class PasswordResetRequestEmail(generics.GenericAPIView):
    """
    Sends an email to the user email address with a link to reset password.

    @PARAMETERS:
     - email
    """
    serializer_class = ResetPasswordSerializer

    def post(self, request, format=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.DATA)
        if serializer.is_valid():
            # print serializer.data['email']
            PasswordReset.objects.send_email_with_reset_instructions(serializer.data['email'])
            response = {'status':'success' , 'response': 'An email containing instructions to reset your password has been sent to {}'.format(request.DATA.get('email'))}
            return Response(response)
        return Response(serializer.errors, status=400)

    def permission_denied(self, request):
        raise exceptions.PermissionDenied("You can't reset your password if you are already authenticated")


class HelpTicketView(mixins.UserRequired,generics.CreateAPIView):
    """
    View for creating a help ticket
    """

    model = HelpTicket
    serializer_class = HelpTicketSerializer

    def perform_create(self, serializer):
        # Include the owner attribute directly, rather than from request data.

        instance = serializer.save(user=self.request.user)
        from django.conf import settings
        from django.core.mail import send_mail

        send_mail('Help ticket raised', '', settings.DEFAULT_FROM_EMAIL, ['renjithraj2005@gmail.com'])
    def pre_save(self, obj):
        """
        Set the ticket's owner, based on the incoming request.
        """
        from django.conf import settings
        from django.core.mail import send_mail

        obj.user = self.request.user
        send_mail('Help ticket raised', '', settings.DEFAULT_FROM_EMAIL, ['admin@eatio.co'])


class AccountPassword(mixins.UserRequired,generics.GenericAPIView):
    """
    Change password of the current user.

    **Accepted parameters:**

     * current_password
     * password
    """

    serializer_class = ChangePasswordSerializer

    def post(self, request, format=None):
        """ validate password change operation and return result """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.DATA, instance=request.user)

        if serializer.is_valid():
            serializer.save()
            return Response({ 'detail': 'Password successfully changed' })

        return Response(serializer.errors, status=400)
