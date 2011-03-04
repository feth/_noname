from django.conf.urls.defaults import include, patterns
from django.views.generic import DetailView, ListView
from noname.models import CompanyName

urlpatterns = patterns('',
    (r'^$',
     ListView.as_view(
         queryset=CompanyName.objects,
         context_object_name='all_proposed_names',
         template_name='noname/index.html')),
    (r'^detail/(?P<pk>[^/]+)/$',
     DetailView.as_view(
         model=CompanyName,
         context_object_name='companyname',
         template_name='noname/detail.html')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^next/$', 'noname.views.next'),
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
