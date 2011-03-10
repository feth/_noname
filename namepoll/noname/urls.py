from django.conf.urls.defaults import patterns, url

#TODO: use direct_to_template when app is ajaxified

urlpatterns = patterns('noname.views',
    url(r'^$', 'index', name='index'),
    url(r'^detail/(?P<pk>[^/]+)/$', 'detail', name='detail'),
    url(r'^otherthan/(?P<name>[^/]+)/$', 'otherthan', name='otherthan'),
    url(r'^random/$', 'otherthan', name='random'),
    url(r'^results/$', 'results', name='results'),
    url(r'^thankyou/$', 'thankyou', name='thankyou'),
)
