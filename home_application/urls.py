# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^demo/$', 'demo'),
    (r'^chart/$', 'chart'),
    (r'^search_business$', 'search_business'),
    (r'^get_task$', 'get_task'),
    (r'^create_task$', 'create_task'),
    (r'^get_app_info$', 'test_la'),
    (r'^get_users$', 'get_users'),
    (r'^ecs_excel_export$', 'ecs_excel_export'),
    (r'^get_top_data$', 'get_top_data'),
    (r'^search_host$', 'search_host'),
    (r'^get_host_data$', 'get_host_data'),
    (r'^search_host_new$', 'search_host_new'),
    (r'^host_performance$', 'host_performance')
)
