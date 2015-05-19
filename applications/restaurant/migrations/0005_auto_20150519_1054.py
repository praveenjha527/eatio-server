# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_restaurant_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lng',
        ),
    ]
