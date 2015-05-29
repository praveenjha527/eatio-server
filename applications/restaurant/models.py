from django.db import models
from django.utils.translation import ugettext_lazy as _

from annoying import functions
from common import base_models
from .foursquare import get_restaurant_details_from_foursquare
from django.conf import settings

class LocationManager(models.Manager):
    def nearby(self, lat, lng, proximity):
        """
        Return all object which distance to specified coordinates
        is less than proximity given in kilometers
        """
        # Great circle distance formula
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(lat))
               * cos(radians(lng) - radians(%s)) +
               sin(radians(%s)) * sin(radians(lat))
              )
              """
        gcd_lt = "{} < %s".format(gcd)
        return self.get_queryset()\
                   .exclude(lat=None)\
                   .exclude(lng=None)\
                   .extra(
                       select={'distance': gcd},
                       select_params=[lat, lng, lat],
                       where=[gcd_lt],
                       params=[lat, lng, lat, proximity],
                       order_by=['distance']
                   )

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
    objects = LocationManager()

    def __unicode__(self):
        return "%s" % (self.name)

    def admin_thumbnail(self):
        if self.image:
            return u'<img src="%s" height = "40" width= "40"/>' % (self.image)
        else:
            return None
    admin_thumbnail.allow_tags=True

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

    @classmethod
    def get_restaurant_results(cls, latitude=None, longitude=None):
        #sample lat and lon (?lat=10.0214997527&lng=76.3446975135)
        restaurants = []
        if latitude and longitude:
            restaurants = cls.objects.nearby(float(latitude), float(longitude), settings.REVIEWS_FETCH_DISTANCE).order_by('-weight')

        return restaurants