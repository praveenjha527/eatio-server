# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('globalprefs', '0003_auto_20150514_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppreferences',
            name='FAQ',
            field=ckeditor.fields.RichTextField(default=b'Frequently Asked Questions'),
            preserve_default=True,
        ),
    ]
