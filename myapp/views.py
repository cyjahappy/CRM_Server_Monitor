from __future__ import unicode_literals

import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponse
from .psutil_get_server_info import get_server_info, server_info_to_database
from .server_info_threshold import *
from .email_alert import *
from .clean_database import clean_database

# 引入Django_Apscheduler库
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 定义全局变量存储服务器各项指标
server_info = dict()
server_info_threshold = dict()

# 实例化调度器(定时获取获取系统各项指标)
scheduler1 = BackgroundScheduler()
# 调度器(定时获取获取系统各项指标)使用默认的DjangoJobStore()
scheduler1.add_jobstore(DjangoJobStore(), 'default')

# 实例化调度器(定时清理数据库过期数据)
scheduler2 = BackgroundScheduler()
# 调度器(定时清理数据库过期数据)使用默认的DjangoJobStore()
scheduler2.add_jobstore(DjangoJobStore(), 'default')


# 定义前端用于获取系统各项指标的API
def server_info_api(request):
    try:
        # 获取全局变量中赋值的变量
        global server_info
        server_info = get_server_info()
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(server_info))


# 定义前端用于获取系统各项指标阈值的API
def server_info_threshold_api(request):
    try:
        # 获取全局变量中赋值的变量
        global server_info_threshold
        server_info_threshold = get_server_info_threshold()
    except Exception as e:
        print(e)
    else:
        return HttpResponse(json.dumps(server_info_threshold))


# 定义前端用于修改系统各项指标报警阈值的API
def modify_threshold_api(request):
    try:
        set_cpu_threshold(request.POST.get('cpu'))
        set_memory_threshold(request.POST.get('memory'))
        set_disk_threshold(request.POST.get('disk'))
        # 每次向数据库中更新数据后, 调用refresh_data()使WEB端重新向数据库中获取一次数据
        refresh_data()
    except Exception as e:
        print(e)
    return HttpResponse('')


# 后端定时获取服务器各项指标(每分钟)
@register_job(scheduler1, 'interval', id='scheduled_get_server_info', minutes=1)
def scheduled_get_server_info():
    # 对全局变量赋值
    global server_info
    global server_info_threshold
    server_info = get_server_info()
    server_info_threshold = get_server_info_threshold()

    # 调用函数将服务器各项指标的值存入数据库
    server_info_to_database(server_info)

    # 检测是否超过阈值
    if (server_info['cpu'] >= server_info_threshold['cpu_threshold']) or (
            server_info['memory'] >= server_info_threshold['memory_threshold']) or (
            server_info['disk'] >= server_info_threshold['disk_threshold']):
        email_alert()
    return


# 每天凌晨3:30的时候自动清除数据库中2天以前当天的所有数据
@register_job(scheduler2, 'cron', id='scheduled_clean_database', hour=3, minute=30)
def scheduled_clean_database():
    clean_database()


# 注册定时任务并开始
register_events(scheduler1)
register_events(scheduler2)
scheduler1.start()
scheduler2.start()


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
