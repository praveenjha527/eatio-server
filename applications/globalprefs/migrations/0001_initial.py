# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apptentive_reward_feedback_frequency', models.PositiveSmallIntegerField(default=5, help_text=b'For Apptentive - After how many times of viewing reward details page should a Reward Feedback be asked in the app')),
                ('google_analytics_send_frequency', models.PositiveSmallIntegerField(default=120, help_text=b'For Google Analytics,  send feedback frequency in seconds')),
                ('first_page', models.CharField(default=b'TIMELINE', max_length=20, choices=[(b'SEARCH', b'SEARCH'), (b'TIMELINE', b'TIMELINE'), (b'NOTIFICATIONS', b'NOTIFICATIONS'), (b'ME', b'ME')])),
                ('show_rewards_with_no_alloted_vouchers_in_list', models.BooleanField(default=False, help_text=b'If True, rewards with no free voucher is also sent to the rewards list page of ios app')),
                ('number_of_feeds_in_page', models.SmallIntegerField(default=10, help_text=b'Number of feeds to be sent to phone per one page fetched by ios app in NEWS page')),
                ('number_of_rewards_in_page', models.SmallIntegerField(default=5, help_text=b'Number of rewards to be sent to phone per one page fetched by ios app in REWARDS page')),
                ('graceful_error_message', models.CharField(default=b'Oh snap, something went wrong', max_length=200)),
                ('terms_and_conditions', ckeditor.fields.RichTextField()),
                ('privacy_policy', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'App Configuration',
                'verbose_name_plural': 'App Configuration',
            },
            bases=(models.Model,),
        ),
    ]
