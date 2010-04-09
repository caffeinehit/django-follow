from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^follow/(?P<app>.*)/(?P<model>.*)/(?P<id>.*)/$', 'follow.views.follow', name = 'follow'),
    url(r'^unfollow/(?P<app>.*)/(?P<model>.*)/(?P<id>.*)/$', 'follow.views.unfollow', name = 'unfollow'),
)
