from __future__ import unicode_literals

import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponse
from .psutil_get_server_info import get_server_info, server_info_to_database
from .server_info_threshold import *
from .email_alert import *
from .clean_database import clean_database
from .database_get_server_info import display_data_minutes
from .database_get_ping_result import display_ping_result_minutes
from .get_ping_result import get_ping_result, ping_result_to_database

# 引入Django_Apscheduler库
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django_apscheduler.models import DjangoJobExecution

# 实例化调度器(定时获取获取系统各项指标)
scheduler1 = BackgroundScheduler()
# 调度器(定时获取获取系统各项指标)使用默认的DjangoJobStore()
scheduler1.add_jobstore(DjangoJobStore(), 'default')

# 实例化调度器(定时清理数据库过期数据)
scheduler2 = BackgroundScheduler()
# 调度器(定时清理数据库过期数据)使用默认的DjangoJobStore()
scheduler2.add_jobstore(DjangoJobStore(), 'default')

# 实例化调度器(定时从PingList数据库中获取ip地址, ping之后将结果存储到PingResults数据库)
scheduler3 = BackgroundScheduler()
# 调度器(定时清理数据库过期数据)使用默认的DjangoJobStore()
scheduler3.add_jobstore(DjangoJobStore(), 'default')


# 定义前端用于实时获取系统各项指标的API
def server_info_api(request):
    try:
        server_info = get_server_info()
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(server_info))


# 定义前端用于实时获取系统各项指标阈值的API
def server_info_threshold_api(request):
    try:
        server_info_threshold = get_server_info_threshold()
    except Exception as e:
        print(e)
    else:
        return HttpResponse(json.dumps(server_info_threshold))


# 定义前端用于实时获取指定IP的Ping结果的API
def ping_result_api(request):
    try:
        ping_result = get_ping_result(request.POST.get('server_ip'))
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(ping_result))


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


# Dashboard的页面
def dashboard(request):
    server_info_minutes = display_data_minutes()
    ping_results_minutes = display_ping_result_minutes()
    data = {
        'cpu_data': server_info_minutes['cpu'],
        'memory_data': server_info_minutes['memory'],
        'disk_data': server_info_minutes['disk'],
        'network_data': server_info_minutes['network'],
        'date': server_info_minutes['date']
    }
    ping_data = {
        'server_ip_id': ping_results_minutes['server_ip_id'],
        'ping_result': ping_results_minutes['ping_result'],
        'date': ping_results_minutes['date']
    }
    return render(request, 'Dashboard.html', locals())


# 测试Bootstrap
def testBootstrap(request):
    return render(request, 'test.html', locals())


# 后端定时获取服务器各项指标(每分钟)
@register_job(scheduler1, 'interval', id='scheduled_get_server_info', minutes=1)
def scheduled_get_server_info():
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
    # 清理ServerInfo数据库的内容
    clean_database()

    # 清理 job executions older than 7 days
    DjangoJobExecution.objects.delete_old_job_executions(604_800)
    return


# 后端定时获取ping各个服务器的结果并存入数据库(每分钟)
@register_job(scheduler3, 'interval', id='scheduled_get_ping_result', minutes=1)
def scheduled_get_ping_result():
    ping_result_to_database()
    return


# 注册定时任务并开始
register_events(scheduler1)
register_events(scheduler2)
register_events(scheduler3)
scheduler1.start()
scheduler2.start()
scheduler3.start()


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
