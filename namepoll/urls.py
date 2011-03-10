from django.conf.urls.defaults import include, patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^noname/', include('noname.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )
#redirect general index
urlpatterns += patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/noname/'}),
    )

