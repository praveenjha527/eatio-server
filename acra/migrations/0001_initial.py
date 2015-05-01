# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrashReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stack_trace', models.TextField(default=b'')),
                ('logcat', models.TextField(default=b'')),
                ('shared_preferences', models.TextField(default=b'')),
                ('environment', models.TextField(default=b'')),
                ('total_mem_size', models.BigIntegerField(default=0, verbose_name=b'Total Memory Size')),
                ('initial_configuration', models.TextField(default=b'')),
                ('display', models.TextField(default=b'')),
                ('available_mem_size', models.BigIntegerField(default=0, verbose_name=b'Available Memory Size')),
                ('phone_model', models.CharField(default=b'', max_length=50)),
                ('user_comment', models.TextField(default=b'')),
                ('crash_configuration', models.TextField(default=b'')),
                ('device_features', models.TextField(default=b'')),
                ('settings_system', models.TextField(default=b'', verbose_name=b'System Settings')),
                ('file_path', models.CharField(default=b'', max_length=100)),
                ('installation_id', models.CharField(default=b'', max_length=100)),
                ('user_crash_date', models.CharField(default=b'', max_length=50, verbose_name=b'Crash Date')),
                ('app_version_name', models.CharField(default=b'', max_length=50, verbose_name=b'Version Name')),
                ('user_app_start_date', models.CharField(default=b'', max_length=50, verbose_name=b'Application Start Date')),
                ('settings_global', models.TextField(default=b'', verbose_name=b'Global Settings')),
                ('build', models.TextField(default=b'')),
                ('settings_secure', models.TextField(default=b'', verbose_name=b'Secure Settings')),
                ('dumpsys_meminfo', models.TextField(default=b'')),
                ('user_email', models.CharField(default=b'', max_length=50)),
                ('report_id', models.CharField(default=b'', max_length=100)),
                ('product', models.CharField(default=b'', max_length=50)),
                ('package_name', models.CharField(default=b'', max_length=100, verbose_name=b'Package Name')),
                ('brand', models.CharField(default=b'', max_length=50)),
                ('android_version', models.CharField(default=b'', max_length=50)),
                ('app_version_code', models.CharField(default=b'', max_length=50, verbose_name=b'Version Code')),
                ('is_silent', models.CharField(default=b'', max_length=50)),
                ('custom_data', models.TextField(default=b'')),
                ('description', models.TextField(default=b'')),
                ('solved', models.CharField(default=b'unsolved', max_length=10, verbose_name=b'Status', choices=[(b'solved', b'Solved'), (b'unsolved', b'Unsolved')])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
