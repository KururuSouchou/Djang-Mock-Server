from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apitest.views.app_list', name='applist'),
    url(r'^', include('apitest.urls')),
    # url(r'^api/', include('apitest.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
