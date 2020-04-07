# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


@admin.register(ServerInfoThreshold)
class ServerInfoThresholdAdmin(admin.ModelAdmin):
    list_display = ['server_name', 'cpu_threshold', 'memory_threshold', 'disk_threshold']
