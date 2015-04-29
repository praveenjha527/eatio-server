# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(default=b'info', max_length=20, choices=[(b'success', b'success'), (b'info', b'info'), (b'warning', b'warning'), (b'error', b'error')])),
                ('unread', models.BooleanField(default=True)),
                ('actor_object_id', models.CharField(max_length=255)),
                ('verb', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('target_object_id', models.CharField(max_length=255, null=True, blank=True)),
                ('action_object_object_id', models.CharField(max_length=255, null=True, blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('public', models.BooleanField(default=True)),
                ('badge', models.PositiveIntegerField(help_text=b'New application icon badge number. Set to None if the badge number must not be changed. At the time of notification creation, this is set only, and set equal to the number of unseen notifications at that time + 1', null=True, blank=True)),
                ('sound', models.CharField(help_text=b'Name of the sound to play. Leave empty if no sound should be played.', max_length=30, blank=True)),
                ('custom_payload', models.CharField(help_text=b'JSON representation of an object containing custom payload.', max_length=240, blank=True)),
                ('type', models.CharField(default=b'GENERAL', max_length=100, choices=[(b'GENERAL', b'GENERAL'), (b'FROM_ADMIN', b'FROM_ADMIN'), (b'RECEIVED POINTS', b'RECEIVED POINTS')])),
                ('action_object_content_type', models.ForeignKey(related_name='notify_action_object', blank=True, to='contenttypes.ContentType', null=True)),
                ('actor_content_type', models.ForeignKey(related_name='notify_actor', to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('target_content_type', models.ForeignKey(related_name='notify_target', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-timestamp',),
            },
            bases=(models.Model,),
        ),
    ]
