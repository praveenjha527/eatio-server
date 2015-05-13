from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import math

from stdimage import StdImageField
from notifications import notify

from common import base_models
from notifications.models import Notification


class LocationManager(models.Manager):
    def nearby(self, latitude, longitude, proximity):
        """
        Return all object which distance to specified coordinates
        is less than proximity given in kilometers
        """
        # Great circle distance formula
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(latitude))
               * cos(radians(longitude) - radians(%s)) +
               sin(radians(%s)) * sin(radians(latitude))
              )
              """
        gcd_lt = "{} < %s".format(gcd)
        return self.get_queryset()\
                   .exclude(latitude=None)\
                   .exclude(longitude=None)\
                   .extra(
                       select={'distance': gcd},
                       select_params=[latitude, longitude, latitude],
                       where=[gcd_lt],
                       params=[latitude, longitude, latitude, proximity],
                       order_by=['distance']
                   )


class Review(base_models.TimeStampedModelBase):
    """
    Review of a user goes here
    good will be True if it is a good comment
    """
    restaurant = models.ForeignKey("restaurant.Restaurant")
    user = models.ForeignKey("accounts.User")
    review = models.TextField(_("Review"))
    good = models.BooleanField(_("Good?"), default=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    image = StdImageField(
        upload_to="review",
        help_text='The image should be atleast 150x100.',
        blank=True,
        max_length=500,
        variations={'large': (450, 300,), 'medium': (300, 200,),},
        null=True
    )

    objects = LocationManager()

    def __unicode__(self):
        return "%s-%s" % (self.restaurant, self.user)

    @classmethod
    def get_valid_reviews(cls, restaurant=None):
        hours_before_time = timezone.now() - timedelta(hours=settings.REVIEWS_HOURS_COUNT)
        reviews = cls.objects.nearby(10.0214997527,76.3446975135,3).filter(created__gte=hours_before_time)
        if restaurant:
            reviews = reviews.filter(restaurant=restaurant)
        return reviews

    @classmethod
    def get_user_reviews(cls, user):
        reviews = cls.objects.filter(user=user)
        return reviews


class AgreeDisagree(base_models.TimeStampedModelBase):
    """
    Agree and disagree of other users saved here
    """
    review = models.ForeignKey(Review, related_name="agree_disagrees")
    user = models.ForeignKey("accounts.User")
    agree = models.BooleanField(_("Agree?"), default=True)

    class Meta:
        unique_together = ("review", "user")

    def __unicode__(self):
        return "%s Review %s by %s" % (
            self.review, unicode(self.get_agree_disagree_text()), self.user)

    def get_agree_disagree_text(self):
        return _("agree") if self.agree else _("disagree")


    def save(self, *args, **kwargs):
        """
        Create like instance and increased like counts by 1.
        :param args:
        :param kwargs:
        :return:
        """
        like = super(AgreeDisagree, self).save(*args, **kwargs)
        self._send_notification(self.user, self.review.user)
        return like

    def _send_notification(self, sender, recipient):
        """
        Send notification to recipient while someone like the selfie.
        """

        if self.get_agree_disagree_text() == 'agree':
            text_type = Notification.NOTIFICATION_TYPE_AGREE
        else:
            text_type = Notification.NOTIFICATION_TYPE_DIS_AGREE

        notify.send(sender, recipient=recipient, verb="%s %s your review @ %s" %(
            sender.name, self.get_agree_disagree_text(), self.review.restaurant),
                    action_object=self, target=self.review, type=text_type)


from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)