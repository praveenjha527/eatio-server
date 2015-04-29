# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150418_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(default=b'', max_length=3000, verbose_name=b'Help and support comment or question')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('temp_key', models.CharField(max_length=100, verbose_name=b'temp_key')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow, verbose_name=b'timestamp')),
                ('reset', models.BooleanField(default=False, verbose_name=b'reset yet?')),
                ('user', models.ForeignKey(verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'password reset',
                'verbose_name_plural': 'password resets',
            },
            bases=(models.Model,),
        ),
    ]
