from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.views.generic import ListView
from noname.models import CompanyName


##FIXME: VERY DIRTY: I just wanna serve jquery.js
##We'll use a static files server
#def _getfile(request, filename):
#    print u"noname/%s" % filename
#    kwargs = {}
#    if filename.endswith(".js"):
#        kwargs['mimetype'] = 'text/javascript'
#    elif filename.endswith(".gif"):
#        kwargs['mimetype'] = 'image/gif'
#    return render_to_response(u"noname/%s" % filename, **kwargs)

urlpatterns = patterns('',
    (r'^$', 'noname.views.index'),
    (r'^detail/(?P<pk>[^/]+)/$', 'noname.views.detail'),
    (r'^evaluate/(?P<pk>[^/]+)/$', 'noname.views.evaluate'),
    (r'^next/$', 'noname.views.next'),
    (r'^thankyou/$', 'noname.views.thankyou'),
#    #FIXME: VERY DIRTY: see above
#    (r'^(.*)$', _getfile)
)
