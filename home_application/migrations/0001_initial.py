# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_ip', models.CharField(max_length=200)),
                ('biz_id', models.CharField(max_length=200)),
                ('host_mem', models.CharField(max_length=200)),
                ('host_disk', models.CharField(max_length=200)),
                ('host_cpu', models.CharField(max_length=200)),
                ('create_time', models.CharField(default=b'2019-07-06 17:50:00', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MonitorHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_ip', models.CharField(max_length=200)),
                ('biz_ip', models.CharField(max_length=200)),
                ('is_monitor', models.BooleanField(default=True)),
            ],
        ),
    ]
