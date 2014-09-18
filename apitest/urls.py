from django.conf.urls import patterns, url
from .views import reg, log_in, log_out, new_app, new_api, ApiUpdate, ApiDelete, list_by_app, apiview, detail, app_list, AppUpdate, AppDelete, success, loglist, dellog
urlpatterns = patterns('',
    url(r'^$', app_list, name='applist'),
    url(r'^app/(?P<app_id>\d+)/$', list_by_app, name='apilist'),
    url(r'^api/(?P<api_id>\d+)/$', detail, name='detail'),
    url(r'^newapp/$', new_app, name='newapp'),
    url(r'^(?P<app_name>\S+)/new_api/$', new_api, name='newapi'),
    url(r'^app/(?P<pk>\d+)/update/$', AppUpdate.as_view(), name='appupdate'),
    url(r'^api/(?P<pk>\d+)/update/$', ApiUpdate.as_view(), name='apiupdate'),
    url(r'^app/(?P<pk>\d+)/delete/$', AppDelete.as_view(), name='appdelete'),
    url(r'^api/(?P<pk>\d+)/delete/$', ApiDelete.as_view(), name='apidelete'),
    url(r'^logs/(?P<app_id>\d+)/$', loglist, name='loglist'),
    url(r'^logs/(?P<app_id>\d+)/delete/$', dellog, name='dellog'),
    # url(r'^logs/log/(?P<log_id>\d+)/$', loglist, name='logdetail'),
    # url(r'^apiview/(?P<app_name>\w+)/(?P<url_path>\S+)$', apiview, name='apiview'),
    url(r'^apiview/(?P<app_name>\w+)/(?P<url_path>\S+)$', apiview, name='apiview'),
    url(r'^reg/$', reg, name='reg'),
    url(r'^login/$', log_in, name='login'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^success/$', success, name='success'),

)
