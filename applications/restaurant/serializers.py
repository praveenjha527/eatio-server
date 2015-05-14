# -*- coding: utf-8 -*-
"""
API serializer classes for profile
"""

from rest_framework import serializers
from applications.review import models as review_models
from applications.restaurant import models as restaurant_models
from applications.review.models import Review, AgreeDisagree
from geopy.distance import vincenty
import os


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant
    """
    away = serializers.SerializerMethodField()
    agree = serializers.SerializerMethodField()
    disagree = serializers.SerializerMethodField()
    latestImg = serializers.SerializerMethodField()
    http_method_names = ["get"]

    class Meta:
        model = restaurant_models.Restaurant
        fields = ('id', 'external_id', 'name', 'image', 'address', 'city', 'country', 'distance', 'weight', 'away', 'lat', 'lng', 'agree', 'disagree', 'latestImg')
        read_only_fields = ('id', )

    def get_away(self, obj):
        request = self.context.get('request')
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        current_location = (lat, lng)
        restaurant_location = (obj.lat, obj.lng)
        return vincenty(current_location, restaurant_location).meters

    def get_agree(self, obj):
        reviews = review_models.Review.objects.filter(restaurant=obj)
        for review in reviews:
            # review total agree_count and disagree_count
            agree_count = AgreeDisagree.objects.filter(review=review, agree=True).count()
            return agree_count

    def get_disagree(self, obj):
        reviews = review_models.Review.objects.filter(restaurant=obj)
        for review in reviews:
            # review total agree_count and disagree_count
            disagree_count = AgreeDisagree.objects.filter(review=review, agree=False).count()
            return disagree_count

    def get_latestImg(self, obj):
        try:
            review = review_models.Review.objects.filter(restaurant=obj).exclude(image='').latest('created')
            imgurl = review.image.url
            return os.path.abspath(imgurl)
        except Exception:
            return "non"


class RestaurantDetailSerializer(RestaurantSerializer):
    reviews = serializers.SerializerMethodField()
    away = serializers.SerializerMethodField()

    class Meta:
        model = restaurant_models.Restaurant
        fields = RestaurantSerializer.Meta.fields+('reviews', 'away')
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
        restaurant_location = (obj.lat, obj.lng)
        return vincenty(current_location, restaurant_location).meters



