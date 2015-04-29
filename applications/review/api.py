# -*- coding: utf-8 -*-
"""
API view for review
"""
from rest_framework import viewsets

from applications.review import serializers
from applications.review import models as review_models
from common import mixins


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
        return review_models.Review.get_valid_reviews()


class AgreeDisagreeViewSet(mixins.UserRequired, viewsets.ModelViewSet):
    """
    Agree and disagree
    """
    http_method_names = ['post',]
    serializer_class = serializers.AgreeDisagreeSerializer
    queryset = review_models.AgreeDisagree.objects.all()

    def perform_create(self, serializer):
        """
        create instance.
        """
        serializer.save(user=self.request.user)
