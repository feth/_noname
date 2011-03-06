from django.conf.urls.defaults import patterns
from django.views.generic import ListView
from noname.models import CompanyName

urlpatterns = patterns('',
    (r'^$', 'noname.views.index'),
    (r'^detail/(?P<pk>[^/]+)/$', 'noname.views.detail'),
    (r'^evaluate/(?P<pk>[^/]+)/$', 'noname.views.evaluate'),
    (r'^next/$', 'noname.views.next'),
    (r'^thankyou/$', 'noname.views.thankyou'),
    #FIXME: VERY DIRTY: I just wanna serve jquery.js
    #but I don't have internet access to see how to serve
    #static files
    #Also, the mime type is html and should be text
    (r'^jquery.js$',
     ListView.as_view(
         queryset=CompanyName.objects,
         context_object_name='all_proposed_names',
         template_name='noname/jquery.js')),
)
