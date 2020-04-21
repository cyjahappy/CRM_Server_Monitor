# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# 这个模型暂时没用
class ServerInfoThreshold(models.Model):
    id = models.AutoField(primary_key=True)
    server_name = models.CharField(default="", max_length=20)
    cpu_threshold = models.FloatField(default=99.0)
    memory_threshold = models.FloatField(default=99.0)
    disk_threshold = models.FloatField(default=99.0)


# 存储系统各项阈值的数据
class FullServerInfoThreshold(models.Model):
    id = models.AutoField(primary_key=True)
    server_name = models.CharField(default="", max_length=20)
    cpu_threshold = models.FloatField(default=99.0)
    memory_threshold = models.FloatField(default=99.0)
    disk_threshold = models.FloatField(default=99.0)
    bandwidth_threshold = models.FloatField(default=99.0)


# 存储系统各项指标的数据
class ServerInfo(models.Model):
    date = models.DateTimeField(primary_key=True, auto_now=True)
    cpu = models.FloatField(null=True)
    memory = models.FloatField(null=True)
    disk = models.FloatField(null=True)
    network = models.FloatField(null=True)
    network_recv = models.FloatField(null=True)
    network_sent = models.FloatField(null=True)


# 存储需要Ping的列表
class PingList(models.Model):
    server_ip = models.GenericIPAddressField(primary_key=True)
    server_name = models.CharField(null=True, max_length=20)


# 存储Ping的结果
class PingResults(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.ForeignKey(PingList, on_delete=models.CASCADE)
    ping_result = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True, null=True)
