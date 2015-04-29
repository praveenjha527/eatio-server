# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=stdimage.models.StdImageField(default=b'/static/assets/images/default_user_image.jpg', help_text=b'The image should be atleast 100x100 and a square.', max_length=500, upload_to=b'userprofile', blank=True),
            preserve_default=True,
        ),
    ]
