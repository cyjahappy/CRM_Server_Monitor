# -*- coding: utf-8 -*-
import psutil
import time


#  网络的单位有问题


def get_server_info():
    cpu = psutil.cpu_percent(interval=1)  # CPU使用率
    memory = float(psutil.virtual_memory().used) / float(psutil.virtual_memory().total) * 100.0  # 内存使用率
    last_disk = (psutil.disk_io_counters(perdisk=False).read_bytes + psutil.disk_io_counters(
        perdisk=False).write_bytes) / 1024.0 / 1024.0  # 直到当前服务器硬盘已经读取和写入的bytes总和
    last_network = (
                               psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv) / 1024.0 / 102.4  # 直到当前服务器网络已经上传和下载的bytes总和
    time.sleep(1)
    network_recv = psutil.net_io_counters().bytes_recv / 1024.0 / 102.4  # 直到当前服务器网络已经上传的MB
    network_sent = psutil.net_io_counters().bytes_sent / 1024.0 / 102.4  # 直到当前服务器网络已经下载的MB

    # 获取需要使用"df -h"命令 to list all mounted disk partitions, 然后选择对的那个来获取磁盘使用率
    disk = psutil.disk_usage("/System/Volumes/Data").percent

    network = network_sent + network_recv - last_network  # 得到这一秒服务器网络上传和下载的总和 单位MB
    server_info = {'cpu': cpu,
                   'memory': memory,
                   'network': network,
                   'network_recv': network_recv,
                   'network_sent': network_sent,
                   'disk': disk
                   }
    return server_info
