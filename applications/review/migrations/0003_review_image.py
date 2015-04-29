# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20150418_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='image',
            field=stdimage.models.StdImageField(help_text=b'The image should be atleast 150x100.', max_length=500, null=True, upload_to=b'review', blank=True),
            preserve_default=True,
        ),
    ]
