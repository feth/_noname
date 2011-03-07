from django.conf.urls.defaults import patterns

#TODO: use direct_to_template when app is ajaxified

urlpatterns = patterns('noname.views',
    (r'^$', 'index'),
    (r'^detail/(?P<pk>[^/]+)/$', 'detail'),
    (r'^evaluate/(?P<pk>[^/]+)/$', 'evaluate'),
    (r'^next/$', 'next'),
    (r'^thankyou/$', 'thankyou'),
)
