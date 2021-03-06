# 使用datetime模块中的datetime类
from datetime import datetime, timedelta
from .models import ServerInfo, PingResults

# 自动清理数据库中今日日期-2天的那天当天的所有数据
number_of_days = 2


def clean_database():
    global number_of_days

    # 获取今天的日期
    now = datetime.now()

    # 获取要清理数据的当天的日期
    date_to_clean = now - timedelta(days=number_of_days)

    # 逐个提取年月日
    date_to_clean_year = (date_to_clean.strftime('%Y'))
    date_to_clean_month = (date_to_clean.strftime('%m'))
    date_to_clean_day = (date_to_clean.strftime('%d'))

    # 获取当天数据的QuerySet
    ServerInfoData = ServerInfo.objects.filter(date__year=date_to_clean_year,
                                               date__month=date_to_clean_month,
                                               date__day=date_to_clean_day)
    PingResultsData = PingResults.objects.filter(date__year=date_to_clean_year,
                                                 date__month=date_to_clean_month,
                                                 date__day=date_to_clean_day)

    # 如果QuerySet不为空, 则删除QuerySet对应的数据
    if ServerInfoData.exists():
        ServerInfoData.delete()
    if PingResultsData.exists():
        PingResultsData.delete()

    return
