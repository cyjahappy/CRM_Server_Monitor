from .models import PingResults, PingList
from datetime import datetime, timedelta

number_of_data = 10

def display_ping_result_minutes():
    # 获取今天的日期
    now = datetime.now()
    database_ping_info_minutes = {
        'server_ip_id': [],
        'ping_result': [],
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
        PingResultsData = PingResults.objects.filter(date__year=date_to_get_data_year,
                                                     date__month=date_to_get_data_month,
                                                     date__day=date_to_get_data_day,
                                                     date__hour=date_to_get_data_hour,
                                                     date__minute=date_to_get_data_minute,
                                                     server_ip_id='14.215.177.39')

        # 只有QuerySet不为空,才会进行取值
        if PingResultsData.exists():
            # PingResultsData[0]从这个QuerySet中获取第一个值(避免像旧方法那样会取到重复值)
            database_ping_info_minutes['server_ip_id'].append(PingResultsData[0].server_ip_id)
            database_ping_info_minutes['ping_result'].append(PingResultsData[0].ping_result)
            database_ping_info_minutes['date'].append(PingResultsData[0].date.strftime('%H:%M'))

        i = i - 1
    return database_ping_info_minutes
