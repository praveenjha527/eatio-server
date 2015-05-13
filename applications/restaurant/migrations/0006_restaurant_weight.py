# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_remove_restaurant_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
