import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.signals import post_save
from model_utils import managers, Choices
from push_notifications.models import APNSDevice, GCMDevice
from applications.utils.decorators import disable_for_loaddata

from .utils import id2slug
from notifications import notify


now = datetime.datetime.now
if getattr(settings, 'USE_TZ'):
    try:
        from django.utils import timezone
        now = timezone.now
    except ImportError:
        pass


class NotificationQuerySet(models.query.QuerySet):
    
    def unread(self):
        "Return only unread items in the current queryset"
        return self.filter(unread=True)
    
    def read(self):
        "Return only read items in the current queryset"
        return self.filter(unread=False)
    
    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store 
        # the time they were marked as read.
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        
        qs.update(unread=False)
    
    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        qs = self.read()
        
        if recipient:
            qs = qs.filter(recipient=recipient)
            
        qs.update(unread=True)

class Notification(models.Model):
    """
    Action model describing the actor acting out a verb (on an optional
    target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>

    Examples::

        <justquick> <reached level 60> <1 minute ago>
        <brosner> <commented on> <pinax/pinax> <2 hours ago>
        <washingtontimes> <started follow> <justquick> <8 minutes ago>
        <mitsuhiko> <closed> <issue 70> on <mitsuhiko/flask> <about 2 hours ago>

    Unicode Representation::

        justquick reached level 60 1 minute ago
        mitsuhiko closed issue 70 on mitsuhiko/flask 3 hours ago

    HTML Representation::

        <a href="http://oebfare.com/">brosner</a> commented on <a href="http://github.com/pinax/pinax">pinax/pinax</a> 2 hours ago

    """

    NOTIFICATION_TYPE_GENERAL = 'GENERAL'
    NOTIFICATION_TYPE_FROM_ADMIN = 'FROM_ADMIN'
    NOTIFICATION_TYPE_RECEIVED_POINTS = 'RECEIVED POINTS'

    NOTIFICATION_TYPE_CHOICES = (
        (NOTIFICATION_TYPE_GENERAL, NOTIFICATION_TYPE_GENERAL ),
        (NOTIFICATION_TYPE_FROM_ADMIN, NOTIFICATION_TYPE_FROM_ADMIN),
        (NOTIFICATION_TYPE_RECEIVED_POINTS, NOTIFICATION_TYPE_RECEIVED_POINTS),
    )


    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default='info', max_length=20)
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False)

    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor')
    actor_object_id = models.CharField(max_length=255)
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target',
        blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type',
        'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType,
        related_name='notify_action_object', blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True,
        null=True)
    action_object = generic.GenericForeignKey('action_object_content_type',
        'action_object_object_id')

    timestamp = models.DateTimeField(default=now)

    public = models.BooleanField(default=True)
    is_push_notification_send = models.BooleanField(default=False)

    badge = models.PositiveIntegerField(null=True, blank=True,
                                        help_text='New application icon badge number. Set to None if the badge number must not be changed. At the time of notification creation, this is set only, and set equal to the number of unseen notifications at that time + 1')
    sound = models.CharField(max_length=30, blank=True,
                             help_text='Name of the sound to play. Leave empty if no sound should be played.')
    custom_payload = models.CharField(max_length=240, blank=True,
                                      help_text='JSON representation of an object containing custom payload.')

    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE_CHOICES, default=NOTIFICATION_TYPE_GENERAL)

    objects = managers.PassThroughManager.for_queryset_class(NotificationQuerySet)()

    class Meta:
        ordering = ('-timestamp', )

    def __unicode__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.target:
            if self.action_object:
                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
            return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx
        if self.action_object:
            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx
        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return id2slug(self.id)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

    def mark_as_pushed(self):
        self.unread = False
        self.is_push_notification_send = True
        self.save()

    def send_push_notification(self):
        """
        Sends push notification in a device was found and returns True
        else returns False
        """

        print "sending"
        device = GCMDevice.objects.get(user=self.recipient)
        print "android -----------"
        print device
        print self.recipient
        device.send_message(self.verb)
        self.mark_as_pushed()
        return True

EXTRA_DATA = False
if getattr(settings, 'NOTIFY_USE_JSONFIELD', False):
    try:
        from jsonfield.fields import JSONField
    except ImportError:
        raise ImproperlyConfigured("You must have a suitable JSONField installed")
    
    JSONField(blank=True, null=True).contribute_to_class(Notification, 'data')
    EXTRA_DATA = True


def notify_handler(verb, **kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """

    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    type = kwargs.pop('type')

    newnotify = Notification(
        recipient = recipient,
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        verb=unicode(verb),
        type=type,
        public=bool(kwargs.pop('public', True)),
        description=kwargs.pop('description', None),
        timestamp=kwargs.pop('timestamp', now())
    )

    for opt in ('target', 'action_object'):
        obj = kwargs.pop(opt, None)
        if not obj is None:
            setattr(newnotify, '%s_object_id' % opt, obj.pk)
            setattr(newnotify, '%s_content_type' % opt,
                    ContentType.objects.get_for_model(obj))
    
    if len(kwargs) and EXTRA_DATA:
        newnotify.data = kwargs

    newnotify.save()


# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')

def create_point_received_notification(sender, recipient, points, for_text):


    text = u'Earned %d points for %s' % (
    points, for_text)

    notify.send(sender, recipient=recipient, verb=text,
                    action_object=recipient, type=Notification.NOTIFICATION_TYPE_RECEIVED_POINTS)


def create_bonus_point_received_notification(sender, recipient):

    from eatio_web.settings import base as settings
    text = u'Earned %d points as Joining Bonus' % ( settings.SIGNUP_BONUS )
    recipient.total_points = recipient.total_points + settings.SIGNUP_BONUS
    recipient.redeemable_points = recipient.redeemable_points + settings.SIGNUP_BONUS
    recipient.save()
    newnotify = Notification(
        recipient = recipient,
        actor_content_type=ContentType.objects.get_for_model(sender),
        actor_object_id=sender.pk,
        verb=unicode(text),
        type=Notification.NOTIFICATION_TYPE_RECEIVED_POINTS,
        public=True,
        description=None,
        timestamp=now(),
        is_push_notification_send = True,
        unread =False


    )
    newnotify.save()

def create_bonus_point_notification_for_referrer(sender, recipient, referred_user):
    from eatio_web.settings import base as settings
    text = u'Earned %d points referring %s to Eatio' % (settings.REFERRAL_POINTS, referred_user)

    notify.send(sender, recipient=recipient, verb=text,
                    action_object=recipient, type=Notification.NOTIFICATION_TYPE_RECEIVED_POINTS)


def create_bonus_point_notification_for_referee(sender, recipient, invited_user):
    from eatio_web.settings import base as settings
    text = u'Earned %d points for joining Eatio on inviation of %s' % (settings.REFERRAL_POINTS, invited_user)

    notify.send(sender, recipient=recipient, verb=text,
                    action_object=recipient, type=Notification.NOTIFICATION_TYPE_RECEIVED_POINTS)




@disable_for_loaddata
def post_notification_save_tasks(sender, instance, created=False, **kwargs):
    """
    Does housekeeping tasks after notification is created like sending push notification
    """
    from .tasks import send_push_notification
    if created and not instance.is_push_notification_send:
        send_push_notification.delay(instance)


post_save.connect(post_notification_save_tasks, sender=Notification, dispatch_uid="post_notification_save_tasks")