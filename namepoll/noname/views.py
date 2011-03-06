from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from noname.models import CompanyName, Voter
from noname.forms import EvaluationForm, VoterForm

def next(request):
    from pprint import pprint
    pprint(request.session)
    name = 'Puma'

    #a relative path. We are 'appname/next'
    newpath = '../detail/%s' % name
    return HttpResponseRedirect(newpath)

def detail(request, pk):
    #make a default voter
    request.session.setdefault("voter", Voter())
    #ensure there is a container for seen names
    request.session.setdefault("seen", [])

    companyname = get_object_or_404(CompanyName, pk=pk)
    voter = request.session["voter"]

#    voter.pages_seen.append(companyname)

    evalform = EvaluationForm()
    voterform = VoterForm(request.POST, instance=voter)
#    evalform.save()

    t = loader.get_template('noname/detail.html')
    c = Context({
        'companyname': companyname,
        'voter': voter,
        'evalform': evalform,
        'voterform': voterform,
    })
    return HttpResponse(t.render(c))
