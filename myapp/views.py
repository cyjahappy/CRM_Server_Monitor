from __future__ import unicode_literals

import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponse
from .psutil_get_server_info import get_server_info
from .server_info_threshold import *
from .email_alert import *

server_info = dict()
server_info_threshold = dict()


def server_info_api(request):
    try:
        global server_info
        server_info = get_server_info()
        if server_info['cpu'] >= server_info_threshold['cpu_threshold']:
            email_alert()
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(server_info))


def server_info_threshold_api(request):
    try:
        global server_info_threshold
        server_info_threshold = get_server_info_threshold()
    except Exception as e:
        print(e)
    else:
        return HttpResponse(json.dumps(server_info_threshold))


def modify_threshold_api(request):
    try:
        set_cpu_threshold(request.POST.get('cpu'))
        print('CPU threshold = ', get_server_info_threshold('cpu_threshold'))
        set_memory_threshold(request.POST.get('memory'))
        print('Memory threshold = ', get_server_info_threshold('memory_threshold'))
        set_disk_threshold(request.POST.get('disk'))
        print('Disk threshold = ', get_server_info_threshold('disk_threshold'))
    except Exception as e:
        print(e)
    return HttpResponse('')


@staff_member_required
def server(request):
    try:
        context = {
            'title': u'CRM服务器监控'
        }
    except Exception as e:
        print(e)
    else:
        return render(request, 'server.html', context)


def modify_threshold(request):
    try:
        context = {
            'title': u'CRM服务器阈值修改'
        }
    except Exception as e:
        print(e)
    else:
        return render(request, 'Threshold.html', context)
