# 从数据库中根据时间单位获取系统各项指标的值, 用于前端展示
from .models import ServerInfo
from datetime import datetime, timedelta

# 定义在前端图表中一次性展示的数据量
number_of_data = 10


# 以分钟为单位从数据库中取值
def display_data_minutes():
    global number_of_data
    database_server_info_minutes = {
        'cpu': [],
        'memory': [],
        'disk': [],
        'network': [],
        'network_recv': [],
        'network_sent': [],
        'date': []
    }
    data = ServerInfo.objects.all()
    length = data.count()
    results = data[length - number_of_data:length]

    i = 0
    while i < number_of_data:
        database_server_info_minutes['cpu'].append(results[i].cpu)
        database_server_info_minutes['memory'].append(results[i].memory)
        database_server_info_minutes['disk'].append(results[i].disk)
        database_server_info_minutes['network'].append(results[i].network)
        database_server_info_minutes['network_recv'].append(results[i].network_recv)
        database_server_info_minutes['network_sent'].append(results[i].network_sent)
        database_server_info_minutes['date'].append(results[i].date.strftime('%H:%M'))
        i = i + 1
    return database_server_info_minutes


'''
# 以小时为单位从数据库中取值
def display_data_hours():
    global number_of_data
    # 获取今天的日期
    now = datetime.now()

    # 获取要清理数据的当天的日期
    date_to_clean = now - timedelta(minutes=11)

    # 逐个提取年月日
    date_to_clean_year = (date_to_clean.strftime('%Y'))
    date_to_clean_month = (date_to_clean.strftime('%m'))
    date_to_clean_day = (date_to_clean.strftime('%d'))
'''
