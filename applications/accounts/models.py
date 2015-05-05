from datetime import datetime
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.db.models.signals import pre_delete
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives

from stdimage import StdImageField
from applications.utils.utils import clean_to_email_field

from common.base_models import TimeStampedModelBase
from .fields import CountryField

class User(AbstractUser, TimeStampedModelBase):
    """
    Model extends auth.user and stores more information like city, about me, location etc

    """

    DEFAULT_HOME_CHOICES = (
        ('SEARCH', 'SEARCH'),
        ('TIMELINE', 'TIMELINE'),
        ('NOTIFICATIONS', 'NOTIFICATIONS'),
        ('ME', 'ME'),
    )

    ACTIVITY_LEVEL = (
        ('DEFAULT', 'DEFAULT'),
        ('HYPERACTIVE', 'HYPERACTIVE'),
        ('NOTUSING', 'NOTUSING'),
        ('OCCASIONAL', 'OCCASIONAL'),
    )

    GENDER_CHOICES = (
        ("male", 'Male'),
        ("female", 'Female'),
    )

    name = models.CharField(_("Name"), max_length=255,)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, null=True, blank=True)
    first_page = models.CharField(max_length=20, choices = DEFAULT_HOME_CHOICES, default ='TIMELINE')
    location_city = models.CharField(max_length=50, null=True, blank=True, default="")
    country = CountryField(max_length=50, null=True, blank=True)
    age = models.DateField(blank=True, null=True)
    image = StdImageField(
        upload_to="userprofile",
        help_text='The image should be atleast 100x100 and a square.',
        blank=True,
        default="/static/assets/images/default_user_image.jpg",
        max_length=500,
        variations={'large': (500, 500, True), 'medium': (100, 100, True),},
        null=True
    )

    # Eatio points related fields
    # actually float inside but always send as the floor integer
    total_points = models.FloatField(default = 0, help_text="Total Points", db_index=True)
    redeemable_points = models.FloatField(default = 0, help_text="Redeemable Points", db_index=True)

    # Tracking user engagements
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL, default='DEFAULT')

    def __unicode__(self):
        return self.name or self.username

    def admin_thumbnail(self):
        if self.image:
            return u'<img src="%s" height = "40" width= "40"/>' % (self.image.url)
        else:
            return None
    admin_thumbnail.allow_tags=True





def send_signup_email(new_user):
    """ welcome email """
    html_template = get_template('email_templates/user_signup_html_template.html')
    text_template = get_template('email_templates/user_signup_text_template.txt')

    subject =  u'Welcome to Eatio, %s' % new_user.first_name

    context = Context({'user': new_user})
    text_content = text_template.render(context)
    html_content = html_template.render(context)

    from_email = settings.DEFAULT_FROM_EMAIL
    to = [clean_to_email_field(new_user.email)]

    # Rich email message -  text and HTML
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # print "email sent to %s" % to

    send_mail('New user %s signed up' % new_user, 'Now!', settings.DEFAULT_FROM_EMAIL, ['admin@eatio.co'])

def send_user_delete_email(sender, instance, created=False, **kwargs):
    """ email to tell user that his account got deleted """

    subject = "Your account was deleted."
    message = 'If this was not expected, contact administrator'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])

pre_delete.connect(send_user_delete_email, sender=User)

class PasswordResetManager(models.Manager):

    def send_email_with_reset_instructions(self, email):
        """ create password reset for specified user """

        user = User.objects.get(username=email)
        password_reset_object, temp_key = self.get_password_reset_object(user)
        current_site = Site.objects.get_current()
        subject = "Password reset request for Eatio"
        message = render_to_string("email_templates/password_reset_key_message.html", {
            "user": user,
            "uid": int_to_base36(user.id),
            "temp_key": temp_key,
            "domain": current_site.domain
        })
        mail_stat = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        # print mail_stat
        return password_reset_object

    def get_password_reset_object(self, user):
        unused_reset_key = self.check_for_unused_reset_key(user)
        if unused_reset_key:
            password_reset_object = unused_reset_key[0]
            temp_key = unused_reset_key[0].temp_key
        else:
            temp_key = token_generator.make_token(user)
            password_reset_object = PasswordReset(user=user, temp_key=temp_key, email=user.email)
            password_reset_object.save()
        return password_reset_object, temp_key

    def check_for_unused_reset_key(self, user):
        existing_key = PasswordReset.objects.filter(user=user, reset=False)
        if existing_key:
            return existing_key
        return False

class PasswordReset(models.Model):
    """ Password reset Key """
    user = models.ForeignKey(User, verbose_name="user")
    email = models.EmailField(max_length=75)
    temp_key = models.CharField("temp_key", max_length=100)
    timestamp = models.DateTimeField("timestamp", default=datetime.utcnow)
    reset = models.BooleanField("reset yet?", default=False)
    objects = PasswordResetManager()

    class Meta:
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'

    def __unicode__(self):
        return "{} (key={}, reset={})".format(self.user.username, self.temp_key, self.reset)


class HelpTicket(models.Model):
    '''
    Help and support model
    '''

    user = models.ForeignKey(User)
    comment = models.TextField(max_length=3000, default='', verbose_name='Help and support comment or question')
    time_created = models.DateTimeField(auto_now_add=True)

class SignupCode(models.Model):
    code = models.CharField(max_length=50, default='AQX', help_text='user referral code ', unique=True)
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name='my_profile')

    class Meta:
        verbose_name = 'Signup Code'
        verbose_name_plural = 'Signup Code'