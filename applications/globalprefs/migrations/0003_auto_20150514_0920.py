# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('globalprefs', '0002_auto_20150514_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apppreferences',
            name='textfield',
        ),
        migrations.AddField(
            model_name='apppreferences',
            name='privacy_policy',
            field=ckeditor.fields.RichTextField(default=b'Privacy Policy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apppreferences',
            name='terms_and_conditions',
            field=ckeditor.fields.RichTextField(default=b'Terms and Conditions'),
            preserve_default=True,
        ),
    ]
