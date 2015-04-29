# -*- coding: utf-8 -*-
"""
API serializer classes for profile
"""
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from applications.review import models as review_models
from applications.restaurant import models as restaurant_models


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant
    """
    http_method_names = ["get"]
    class Meta:
        model = restaurant_models.Restaurant
        fields = ('id', 'external_id', 'name', 'image', 'address', 'city', 'country', 'distance')
        read_only_fields = ('id', )


class RestaurantDetailSerializer(RestaurantSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = restaurant_models.Restaurant
        fields = RestaurantSerializer.Meta.fields+('reviews', )
        read_only_fields = ('id', )

    def get_reviews(self, obj):
        from applications.review import serializers as review_serializers
        return [review_serializers.ReviewBaseSerializer(
            instance=review, context=self.context,
            ).data for review in review_models.Review.get_valid_reviews(obj)]



