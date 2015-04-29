# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150423_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passwordreset',
            options={'verbose_name': 'Password Reset', 'verbose_name_plural': 'Password Resets'},
        ),
        migrations.AlterModelOptions(
            name='signupcode',
            options={'verbose_name': 'Signup Code', 'verbose_name_plural': 'Signup Code'},
        ),
    ]
