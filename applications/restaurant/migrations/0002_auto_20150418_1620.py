# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='external_id',
            field=models.CharField(max_length=100, verbose_name='Restaurant external Id', db_index=True),
            preserve_default=True,
        ),
    ]
