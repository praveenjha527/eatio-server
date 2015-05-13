# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_review_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
