from .models import *

# 从数据库中获取CPU使用率
cpu_threshold = ServerInfoThreshold.objects.get(id=1).cpu_threshold

# 从数据库中获取内存使用率
memory_threshold = ServerInfoThreshold.objects.get(id=1).memory_threshold

# 从数据库中获取磁盘使用率
disk_threshold = ServerInfoThreshold.objects.get(id=1).disk_threshold


def get_server_info_threshold(info=None):
    server_info_threshold = {
        'cpu_threshold': float(cpu_threshold),
        'memory_threshold': float(memory_threshold),
        'disk_threshold': float(disk_threshold)
    }

    if info:
        return server_info_threshold[info]
    else:
        return server_info_threshold


def set_cpu_threshold(threshold):
    ServerInfoThreshold.objects.filter(id=1).update(cpu_threshold=threshold)


def set_memory_threshold(threshold):
    ServerInfoThreshold.objects.filter(id=1).update(memory_threshold=threshold)


def set_disk_threshold(threshold):
    ServerInfoThreshold.objects.filter(id=1).update(disk_threshold=threshold)


def refresh_data():
    global cpu_threshold
    global memory_threshold
    global disk_threshold
    cpu_threshold = ServerInfoThreshold.objects.get(id=1).cpu_threshold
    memory_threshold = ServerInfoThreshold.objects.get(id=1).memory_threshold
    disk_threshold = ServerInfoThreshold.objects.get(id=1).disk_threshold
