from datetime import datetime
from random import choice

from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from noname.models import CompanyName, Voter
from noname.forms import EvaluationForm, VoterForm

SESSIONS_EXPIRY = datetime(2011, 12, 31, 23, 59, 59, 999)

def _voter(request):
    """
    does a bunch of things with the request to have a decent voter.
    """
    if "voter" in request.session:
        return request.session["voter"]

    #### Once per session

    #set expiration date
    request.session.set_expiry(SESSIONS_EXPIRY)
    #ensure there is a container for seen names
    request.session.setdefault("seen", [])
    #make a default voter
    voter = Voter()
    voter.save() #so it's guaranteed to have an id
    request.session["voter"] = voter

    return voter


def thankyou(request):
    voter = _voter(request)
    return render_to_response('noname/thankyou.html', {'voter': voter})


def _next(voter):
    allcomp = CompanyName.objects.all()
    remaining = frozenset(allcomp) - frozenset(voter.pages_seen.all())
    if not remaining:
        remaining = frozenset(allcomp) - frozenset(voter.pages_voted.all())
        if not remaining:
            return HttpResponseRedirect("/noname/thankyou/")

    #a relative path. We are 'appname/next'
    newpath = '../detail/%s' % choice(remaining).name
    return HttpResponseRedirect(newpath)


def next(request):
    voter = _voter(request)
    return _next(voter)


def detail(request, pk):
    voter = _voter(request)
    companyname = get_object_or_404(CompanyName, pk=pk)
    voter.pages_seen.add(companyname)

    evalform = EvaluationForm()
    voterform = VoterForm(request.POST, instance=voter)
#    evalform.save()

    template = loader.get_template('noname/detail.html')
    context = RequestContext(request, {
        'companyname': companyname,
        'voter': voter,
        'evalform': evalform,
        'voterform': voterform,
    })
    return HttpResponse(template.render(context))


def evaluate(request, pk):
    voter = _voter(request)
    companyname = get_object_or_404(CompanyName, pk=pk)
    voter.pages_voted.add(companyname)

    return _next(voter)


def index(request):
    voter = _voter(request)
    variables = {
        'voter': voter,
        'all_proposed_names': CompanyName.objects.all(),
        }
    return render_to_response('noname/index.html', variables)
