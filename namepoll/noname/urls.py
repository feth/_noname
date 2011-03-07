from django.conf.urls.defaults import patterns


urlpatterns = patterns('noname.views',
    (r'^$', 'index'),
    (r'^detail/(?P<pk>[^/]+)/$', 'detail'),
    (r'^evaluate/(?P<pk>[^/]+)/$', 'evaluate'),
    (r'^next/$', 'next'),
    (r'^thankyou/$', 'thankyou'),
)
