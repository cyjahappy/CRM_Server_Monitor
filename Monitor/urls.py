from django.urls import path
from django.contrib import admin
from myapp.views import server_info_api, server, server_info_threshold_api, modify_threshold_api, modify_threshold, \
    dashboard, ping_result_api, testBootstrap

urlpatterns = [
    path('admin/', admin.site.urls),

    # 服务器负载查看页面
    path('admin/server', server, name='server'),

    # 服务器阈值修改页面
    path('admin/modify-threshold', modify_threshold, name='modify_threshold'),

    # 获取服务器负载信息API
    path('admin/server-info-api', server_info_api, name='server_info_api'),

    # 获取Ping结果API(用于前端实时更新Line Chart数据)
    path('admin/ping_result_api', ping_result_api, name='ping_result_api'),

    # 获取服务器负载阈值API
    path('admin/server-info-threshold-api', server_info_threshold_api, name='server_info_threshold_api'),

    # 更改阈值API
    path('admin/modify-threshold-api', modify_threshold_api, name='modify_threshold_api'),

    # Dashboard
    path('dashboard', dashboard, name='dashboard'),

    # test
    path('test', testBootstrap),
]
