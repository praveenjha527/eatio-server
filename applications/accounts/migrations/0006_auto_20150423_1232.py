# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_helpticket_passwordreset'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=b'AQX', help_text=b'user referral code  ', unique=True, max_length=50)),
                ('user', models.ForeignKey(verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='activity_level',
            field=models.CharField(default=b'DEFAULT', max_length=20, choices=[(b'DEFAULT', b'DEFAULT'), (b'HYPERACTIVE', b'HYPERACTIVE'), (b'NOTUSING', b'NOTUSING'), (b'OCCASIONAL', b'OCCASIONAL')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='first_page',
            field=models.CharField(default=b'TIMELINE', max_length=20, choices=[(b'SEARCH', b'SEARCH'), (b'TIMELINE', b'TIMELINE'), (b'NOTIFICATIONS', b'NOTIFICATIONS'), (b'ME', b'ME')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='redeemable_points',
            field=models.FloatField(default=0, help_text=b'Redeemable Points', db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='total_points',
            field=models.FloatField(default=0, help_text=b'Total Points', db_index=True),
            preserve_default=True,
        ),
    ]
