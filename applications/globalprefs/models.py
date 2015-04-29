from django.db import models

from solo.models import SingletonModel



class AppPreferences(SingletonModel):

    apptentive_reward_feedback_frequency = models.PositiveSmallIntegerField(default=5, help_text='For Apptentive - After how many times of viewing reward details page should a Reward Feedback be asked in the app')
    google_analytics_send_frequency = models.PositiveSmallIntegerField(default=120, help_text='For Google Analytics,  send feedback frequency in seconds')


    DEFAULT_HOME_CHOICES = (
        ('SEARCH', 'SEARCH'),
        ('TIMELINE', 'TIMELINE'),
        ('NOTIFICATIONS', 'NOTIFICATIONS'),
        ('ME', 'ME'),
    )

    first_page = models.CharField(max_length=20, choices = DEFAULT_HOME_CHOICES, default='TIMELINE')

    show_rewards_with_no_alloted_vouchers_in_list = models.BooleanField(default=False, help_text= 'If True, rewards with no free voucher is also sent to the rewards list page of ios app')
    number_of_feeds_in_page = models.SmallIntegerField(default=10, help_text='Number of feeds to be sent to phone per one page fetched by ios app in NEWS page')
    number_of_rewards_in_page = models.SmallIntegerField(default=5, help_text='Number of rewards to be sent to phone per one page fetched by ios app in REWARDS page')
    graceful_error_message = models.CharField(max_length=200, default= 'Oh snap, something went wrong')



    def __unicode__(self):
        return u"App Configuration"

    class Meta:
        verbose_name = "App Configuration"
        verbose_name_plural = "App Configuration"


