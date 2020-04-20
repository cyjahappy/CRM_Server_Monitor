# 从数据库中根据时间单位获取系统各项指标的值, 用于前端展示
from .models import ServerInfo
from datetime import datetime, timedelta

# 定义在前端图表中一次性展示的数据量
number_of_data = 10

'''
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


# 以分钟为单位从数据库中取值(改良)
def display_data_minutes():
    # 获取今天的日期
    now = datetime.now()
    database_server_info_minutes = {
        'cpu': [],
        'memory': [],
        'disk': [],
        'network': [],
        'network_recv': [],
        'network_sent': [],
        'date': []
    }
    i = number_of_data
    while i > 0:
        date_to_get_data = now - timedelta(minutes=i)
        # 逐个提取年月日
        date_to_get_data_year = (date_to_get_data.strftime('%Y'))
        date_to_get_data_month = (date_to_get_data.strftime('%m'))
        date_to_get_data_day = (date_to_get_data.strftime('%d'))
        date_to_get_data_hour = (date_to_get_data.strftime('%H'))
        date_to_get_data_minute = (date_to_get_data.strftime('%M'))
        # 获取这个时间点的QuerySet
        ServerInfoData = ServerInfo.objects.filter(date__year=date_to_get_data_year,
                                                   date__month=date_to_get_data_month,
                                                   date__day=date_to_get_data_day,
                                                   date__hour=date_to_get_data_hour,
                                                   date__minute=date_to_get_data_minute)

        # 只有QuerySet不为空,才会进行取值
        if ServerInfoData.exists():
            # ServerInfoData[0]从这个QuerySet中获取第一个值(避免像旧方法那样会取到重复值)
            database_server_info_minutes['cpu'].append(ServerInfoData[0].cpu)
            database_server_info_minutes['memory'].append(ServerInfoData[0].memory)
            database_server_info_minutes['disk'].append(ServerInfoData[0].disk)
            database_server_info_minutes['network'].append(ServerInfoData[0].network)
            database_server_info_minutes['network_recv'].append(ServerInfoData[0].network_recv)
            database_server_info_minutes['network_sent'].append(ServerInfoData[0].network_sent)
            database_server_info_minutes['date'].append(ServerInfoData[0].date.strftime('%H:%M'))

        i = i - 1
    return database_server_info_minutes
