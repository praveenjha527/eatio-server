from django.db import models
from django.utils.translation import ugettext_lazy as _

from annoying import functions
from common import base_models
from .foursquare import get_restaurant_details_from_foursquare


class Restaurant(base_models.TimeStampedModelBase):
    external_id = models.CharField(_("Restaurant external Id"), max_length=100, db_index=True)
    name = models.CharField(_("Name"), max_length=255)
    image = models.CharField(_("Image"), max_length=255, null=True, blank=True)
    address = models.CharField(_("Address"), max_length=255,null=True, blank=True)
    city = models.CharField(_("City"), max_length=255,null=True, blank=True)
    country = models.CharField(_("Country"), max_length=255,null=True, blank=True)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    distance = models.CharField(_("Distance"), max_length=30,null=True, blank=True)
    weight = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s" % (self.name)

    @classmethod
    def get_or_create_restaurant(cls, external_id):
        """
        Get details of restaurant and create a instance
        :param restaurant_id:
        :return:
        """
        restaurant = functions.get_object_or_None(cls, external_id=external_id)
        if not restaurant:
            details = get_restaurant_details_from_foursquare(external_id)
            restaurant = cls.objects.create(**details)
        return restaurant