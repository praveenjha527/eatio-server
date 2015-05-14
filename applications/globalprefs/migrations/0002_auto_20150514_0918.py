# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('globalprefs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apppreferences',
            name='privacy_policy',
        ),
        migrations.RemoveField(
            model_name='apppreferences',
            name='terms_and_conditions',
        ),
        migrations.AddField(
            model_name='apppreferences',
            name='textfield',
            field=models.TextField(default=b'testing', help_text=b'test field'),
            preserve_default=True,
        ),
    ]
