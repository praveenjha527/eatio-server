# -*- coding: utf-8 -*-
"""
API view for review
"""

from rest_framework import viewsets
from rest_framework import generics

from applications.review import serializers
from applications.review import models as review_models
from common import mixins
from rest_framework import filters


class ReviewViewSet(mixins.UserRequired, viewsets.ModelViewSet):
    """
    Create a review
    """
    http_method_names = ['post', "get"]
    serializer_class = serializers.ReviewSerializer
    queryset = review_models.Review.objects.all()

    def perform_create(self, serializer):
        """
        create instance.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        latitude = self.request.GET.get('lat', None)
        longitude = self.request.GET.get('lng', None)
        return review_models.Review.get_valid_reviews(None, latitude, longitude, self.request.user)


class ReviewSearchViewSet(mixins.UserRequired, viewsets.ModelViewSet):

    http_method_names = ['get']
    serializer_class = serializers.ReviewSearchSerializer
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        """
        Review Search Function

        #sample key , lat and lon (?key=4&lat=10.0214997527&lng=76.3446975135)
        """
        search = self.request.GET.get('key', None)
        latitude = self.request.GET.get('lat', None)
        longitude = self.request.GET.get('lng', None)
        if None in [search,longitude, latitude]:
            return []
        return review_models.Review.get_search_results(search, latitude, longitude, self.request.user)


class AgreeDisagreeViewSet(mixins.UserRequired, viewsets.ModelViewSet):
    """
    Agree and disagree
    """
    http_method_names = ['post', 'delete', ]
    serializer_class = serializers.AgreeDisagreeSerializer
    queryset = review_models.AgreeDisagree.objects.all()

    def perform_create(self, serializer):
        """
        create instance.
        """
        serializer.save(user=self.request.user)

    def get_object(self):
        """
        Get agreeDisagree object based on review and user
        """
        return generics.get_object_or_404(self.queryset, review_id=self.kwargs.get('pk'), user=self.request.user)




