from django.conf.urls.defaults import patterns, url

#TODO: use direct_to_template when app is ajaxified

urlpatterns = patterns('noname.views',
    url(r'^$', 'index', name='index'),
    url(r'^detail/(?P<pk>[^/]+)/$', 'detail', name='detail'),
    url(r'^eval/(?P<pk>[^/]+)/$', 'eval', name='eval'),
    url(r'^message/(?P<pk>[^/]+)/$', 'message', name='message'),
    url(r'^otherthan/(?P<name>[^/]+)/$', 'otherthan', name='otherthan'),
    url(r'^voterinfo/$', 'voterinfo', name='voterinfo'),
    url(r'^random/$', 'otherthan', name='random'),
    url(r'^results/$', 'results', name='results'),
    url(r'^review/$', 'review', name='review'),
    url(r'^thankyou/$', 'thankyou', name='thankyou'),
    url(r'^logout/$', 'logout', name='logout'),
)
