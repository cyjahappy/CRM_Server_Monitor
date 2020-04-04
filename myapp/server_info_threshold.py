# 服务器各项指标的阈值

# CPU使用率
cpu_threshold = 90

# 内存使用率
memory_threshold = 90

# 磁盘使用率
disk_threshold = 90


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
    global cpu_threshold
    cpu_threshold = threshold


def set_memory_threshold(threshold):
    global memory_threshold
    memory_threshold = threshold


def set_disk_threshold(threshold):
    global disk_threshold
    disk_threshold = threshold
