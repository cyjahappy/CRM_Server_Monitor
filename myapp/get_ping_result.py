from ping3 import ping
from .models import PingList, PingResults


def get_ping_results():
    ip = PingList.objects.all()
    total_ip = ip.count()
    ping_results = {
        'server_name': [],
        'server_ip': [],
        'ping_result': []
    }
    i = 0
    while i < total_ip:
        ping_results['server_name'].append(ip[i].server_name)
        ping_results['server_ip'].append(ip[i].server_ip)
        ping_results['ping_result'].append(ping(ip[i].server_ip))
        i = i + 1
    return ping_results


def ping_result_to_database():
    ip = PingList.objects.all()
    total_ip = ip.count()
    i = 0
    while i < total_ip:
        data = PingResults()
        data.server_ip = ip[i].server_ip
        data.ping_result = ping(ip[i].server_ip)
        data.save()
        i = i + 1
    return
