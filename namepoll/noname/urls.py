from django.conf.urls.defaults import patterns
from django.views.generic import DetailView, ListView
from noname.models import CompanyName

urlpatterns = patterns('',
    (r'^$',
     ListView.as_view(
         queryset=CompanyName.objects,
         context_object_name='all_proposed_names',
         template_name='noname/index.html')),
    (r'^(?P<pk>\d+)/$',
     DetailView.as_view(
         model=CompanyName,
         template_name='noname/detail.html')),
)
