# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150423_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupcode',
            name='code',
            field=models.CharField(default=b'AQX', help_text=b'user referral code ', unique=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signupcode',
            name='user',
            field=models.OneToOneField(related_name='my_profile', verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
