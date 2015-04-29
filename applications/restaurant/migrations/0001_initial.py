# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Modified', editable=False, blank=True)),
                ('external_id', models.CharField(max_length=100, verbose_name='External Id', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('image', models.CharField(max_length=255, null=True, verbose_name='Image', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Address', blank=True)),
                ('city', models.CharField(max_length=255, null=True, verbose_name='City', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
