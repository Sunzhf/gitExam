# -*- coding: utf-8 -*-
from django.db import models


class HostInfo(models.Model):
    host_ip = models.CharField(max_length=200)
    biz_id = models.CharField(max_length=200)
    host_mem = models.CharField(max_length=200)
    host_disk = models.CharField(max_length=200)
    host_cpu = models.CharField(max_length=200)
    create_time = models.CharField(max_length=200, default="2019-07-06 17:50:00")


class MonitorHost(models.Model):
    host_ip = models.CharField(max_length=200)
    biz_ip = models.CharField(max_length=200)
    is_monitor = models.BooleanField(default=True)
