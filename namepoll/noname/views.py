from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from noname.models import CompanyName

def next(request):
    from pprint import pprint
    pprint(request.session)
    name = 'Puma'

    #a relative path. We are 'appname/next'
    newpath = '../detail/%s' % name
    return HttpResponseRedirect(newpath)
