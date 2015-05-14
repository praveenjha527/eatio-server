# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20150419_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
