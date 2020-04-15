# 使用datetime模块中的datetime类
from datetime import datetime, timedelta
from .models import ServerInfo

# 自动清理数据库中今日日期-1天的那天当天的所有数据
number_of_days = 1


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

    # 获取当天数据的实例
    data = ServerInfo.objects.filter(date__year=date_to_clean_year,
                                     date__month=date_to_clean_month,
                                     date__day=date_to_clean_day)

    # 删除数据
    data.delete()

    pass
