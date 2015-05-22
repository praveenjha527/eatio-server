# -*- coding: utf-8 -*-
"""
API serializer classes for profile
"""
from django.utils.translation import ugettext_lazy as _
from django.utils.timesince import timesince

from rest_framework import serializers

from applications.review import models as review_models
from applications.restaurant import models as restaurant_models
from applications.accounts import serializers as accounts_serializer
from applications.restaurant import serializers as restaurant_serializer


class BaseReviewBaseSerializer(serializers.ModelSerializer):
    """
    Serializer for review.Review
    """
    external_id = serializers.CharField(label=_("Restaurant external Id"), max_length=100, write_only=True)
    agree_count = serializers.SerializerMethodField()
    disagree_count = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = review_models.Review
        fields = (
            'id', 'review', 'good', 'external_id', 'agree_count',
            'disagree_count', 'voted', 'time_since', 'image')
        read_only_fields = ('id', )

    def create(self, validated_data):
        """
        Create restaurant and save to review
        """
        restaurant = restaurant_models.Restaurant.get_or_create_restaurant(
            external_id = validated_data["external_id"], )
        del validated_data["external_id"]
        validated_data["restaurant"] = restaurant
        review = super(BaseReviewBaseSerializer, self).create(validated_data)
        review.latitude = float(restaurant.lat)
        review.longitude = float(restaurant.lng)
        review.save()
        return review

    def get_agree_count(self, obj):
        return obj.agree_disagrees.filter(agree=True).count()

    def get_disagree_count(self, obj):
        return obj.agree_disagrees.filter(agree=False).count()

    def get_voted(self, obj):
        return review_models.AgreeDisagree.objects.filter(
            review=obj, user=self.context['request'].user).exists()

    def get_time_since(self, obj):
        return timesince(obj.created)

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.large.url)


class ReviewBaseSerializer(BaseReviewBaseSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = review_models.Review
        fields = BaseReviewBaseSerializer.Meta.fields+ ('user', )
        read_only_fields = ('id', )

    def get_user(self, obj):
        return accounts_serializer.UserSerializer(instance=obj.user, context=self.context).data


class ReviewSerializerForUser(ReviewBaseSerializer):
    """
    Serializer for review.Review with restaurant
    """
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = review_models.Review
        fields = (
            'id', 'review', 'good', 'external_id', 'agree_count',
            'disagree_count', 'voted', 'time_since', 'image','restaurant')
        read_only_fields = ('id', )

    def get_restaurant(self, obj):
        return restaurant_serializer.RestaurantSerializer(instance=obj.restaurant, context=self.context).data


class ReviewSerializer(BaseReviewBaseSerializer):
    """
    Serializer for review.Review with restaurant
    """
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = review_models.Review
        fields = (
            'id', 'review', 'good', 'external_id', 'agree_count',
            'disagree_count', 'voted', 'time_since', 'restaurant', "restaurant", "image")
        read_only_fields = ('id', )

    def get_restaurant(self, obj):
        return restaurant_serializer.RestaurantSerializer(instance=obj.restaurant, context=self.context).data


class AgreeDisagreeSerializer(serializers.ModelSerializer):
    """
    serializer for agree review
    """
    class Meta:
        model = review_models.AgreeDisagree
        fields = ('id', 'user', 'review', 'agree')
        read_only_fields = ('id', )


class ReviewSearchSerializer(serializers.ModelSerializer):
    """
    searializer for Search review
    """
    class Meta:
        model = review_models.Review
