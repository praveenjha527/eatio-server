# -*- coding: utf-8 -*-
"""
API serializer classes for profile
"""
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from applications.review import models as review_models
from applications.restaurant import models as restaurant_models

from geopy.distance import vincenty

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
    away = serializers.SerializerMethodField()

    class Meta:
        model = restaurant_models.Restaurant
        fields = RestaurantSerializer.Meta.fields+('reviews', 'away' )
        read_only_fields = ('id', )

    def get_reviews(self, obj):
        from applications.review import serializers as review_serializers
        return [review_serializers.ReviewBaseSerializer(
            instance=review, context=self.context,
            ).data for review in review_models.Review.get_valid_reviews(obj)]

    def get_away(self, obj):
        request = self.context.get('request')
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        current_location = (lat, lng)
        restaurant_location = (obj.lat,obj.lng)
        return vincenty(current_location, restaurant_location).meters



