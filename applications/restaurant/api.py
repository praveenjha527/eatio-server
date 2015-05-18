# -*- coding: utf-8 -*-
"""
API view for review
"""
from rest_framework import viewsets
from rest_framework.response import Response

from applications.restaurant import serializers
from applications.restaurant import models as restaurant_models
from common import mixins
from .foursquare import FourSquare


class RestaurantViewSet(mixins.UserRequired, viewsets.ModelViewSet):
    """
    Create a review
    """
    lookup_field = "external_id"
    http_method_names = ["get"]
    serializer_class = serializers.RestaurantSerializer
    queryset = restaurant_models.Restaurant.objects.all().order_by('-weight')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        obj = restaurant_models.Restaurant.get_or_create_restaurant(
            external_id = self.kwargs[lookup_url_kwarg] )
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return serializers.RestaurantDetailSerializer if self.kwargs.get(
            lookup_url_kwarg) else serializers.RestaurantSerializer


class RestaurantNearbyViewSet(RestaurantViewSet):
    def list(self, request, *args, **kwargs):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        results = []
        if lat and lng:
            venues = FourSquare().search_venues(lat, lng)
            results = [serializers.RestaurantSerializer(data=venue).initial_data for venue in venues]
        result = {
            "count": len(results),
            "next": None,
            "previous": None,
            "results": results
        }
        return Response(result)