from django.conf.urls.defaults import include, patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^noname/', include('noname.urls')),
    (r'^admin/', include(admin.site.urls)),
    )
