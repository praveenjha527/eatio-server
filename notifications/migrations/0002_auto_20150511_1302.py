# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(default=b'GENERAL', max_length=100, choices=[(b'GENERAL', b'GENERAL'), (b'FROM_ADMIN', b'FROM_ADMIN'), (b'RECEIVED POINTS', b'RECEIVED POINTS'), (b'AGREE', b'AGREE'), (b'DIS_AGREE', b'DIS_AGREE')]),
            preserve_default=True,
        ),
    ]
