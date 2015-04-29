# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20150418_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='country',
            field=models.CharField(max_length=255, null=True, verbose_name='Country', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='distance',
            field=models.CharField(max_length=30, null=True, verbose_name='Distance', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lat',
            field=models.CharField(max_length=30, null=True, verbose_name='Latitude', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lng',
            field=models.CharField(max_length=30, null=True, verbose_name='Longitude', blank=True),
            preserve_default=True,
        ),
    ]
