from django.conf.urls.defaults import include, patterns
#XXX: only works in debug
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^noname/', include('noname.urls')),
    (r'^admin/', include(admin.site.urls)),
    )
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    (r'^.*', include('noname.urls')),
    )

