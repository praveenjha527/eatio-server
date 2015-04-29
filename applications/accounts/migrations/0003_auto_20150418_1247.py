# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150418_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=8, null=True, choices=[(b'male', b'Male'), (b'female', b'Female')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=stdimage.models.StdImageField(default=b'/static/assets/images/default_user_image.jpg', upload_to=b'userprofile', max_length=500, blank=True, help_text=b'The image should be atleast 100x100 and a square.', null=True),
            preserve_default=True,
        ),
    ]
