from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^follow/(?P<username>.*)$', 'follow.views.follow', name = 'follow'),
    url('^unfollow/(?P<username>.*)$', 'follow.views.unfollow', name = 'unfollow'),
    url('^block/(?P<username>.*)$', 'follow.views.block', name = 'block'),
    url('^unblock/(?P<username>.*)$', 'follow.views.unblock', name = 'unblock'),
)
