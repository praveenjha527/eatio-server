# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20150519_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='lat',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lng',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
