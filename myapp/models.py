# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ServerInfoThreshold(models.Model):
    id = models.AutoField(primary_key=True)
    server_name = models.CharField(default="", max_length=20)
    cpu_threshold = models.FloatField(default=99.0)
    memory_threshold = models.FloatField(default=99.0)
    disk_threshold = models.FloatField(default=99.0)


class Meta:
    verbose_name = '服务器报警阈值'
