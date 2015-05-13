# -*- coding: utf-8 -*-
"""
API serializer classes for profile
"""
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


from applications.accounts import models as account_models
from applications.review import models as review_models
from .models import HelpTicket


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for auth.User
    """
    reviews = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    class Meta:
        model = account_models.User
        fields = ('id', 'username', 'name', 'image', 'gender', 'code', 'activity_level', 'total_points', 'redeemable_points', 'country', 'age', 'location_city','reviews')
        read_only_fields = ('id', 'total_points', 'redeemable_points' )

    def get_code(self, obj):
        try:
            return account_models.SignupCode.objects.get(user=obj).code
        except Exception:
            return "admin"

    def get_reviews(self, obj):
        from applications.review import serializers as review_serializers
        return [review_serializers.BaseReviewBaseSerializer(
            instance=review, context=self.context,
            ).data for review in review_models.Review.get_user_reviews(obj)]

    def get_image(self, obj):
        """
        return selfie count
        :param user:  user instance
        :return: count
        """
        return self.context['request'].build_absolute_uri(obj.image.small.url)


class UserRegisterSerializer(UserSerializer):
    """
    User register serializer returns token
    """
    username = serializers.CharField(validators=[UniqueValidator(queryset=account_models.User.objects.all(),
                                                                 message=_('Username Already exists.'))])
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = account_models.User
        fields = ('id', 'username', 'name', 'password', 'image', 'gender', 'token')
        read_only_fields = ('id', )
        write_only_fields = ('password', )

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        """
        return current user instance
        :param validated_data: Serialized valid data.
        :return user instance
        :rtype object
        """
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['email'] = validated_data['username']
        user = super(UserSerializer, self).create(validated_data)
        return user


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    def validate_email(self, data):
        """ ensure email is in the database """
        user = account_models.User.objects.filter(username__iexact=data, is_active=True)
        if user:
            return data
        raise serializers.ValidationError("Email address not verified for any user account")




class HelpTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpTicket
        fields = ('comment',)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Change password serializer
    """
    current_password = serializers.CharField(
        help_text=_('Current Password'),
    )
    password = serializers.CharField(
        help_text=_('New Password'),
    )

    def validate_current_password(self, value):
        """
        current password check
        """
        print self
        if self.instance.has_usable_password() and not self.instance.check_password(value):
            raise serializers.ValidationError(_('Current password is not correct'))

        return value

    def update(self, instance, validated_data):
        """ change password """
        if instance is not None:
            instance.set_password(validated_data.get('password'))
            instance.save()
            return instance

        return instance

