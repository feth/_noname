from datetime import datetime, date
from random import choice

from django.template import RequestContext
from django.template import loader
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from noname.models import CompanyName, Voter, Evaluation
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
    request.session["voter"] = voter.id

    return voter.id


def _next(voter):
    allcomp = CompanyName.objects.all()
    remaining = frozenset(allcomp) - frozenset(voter.pages_seen.all())
    if not remaining:
        remaining = frozenset(allcomp) - frozenset(voter.pages_voted.all())
        if not remaining:
            return HttpResponseRedirect("/noname/thankyou/")

    #a relative path. We are 'appname/next'
    new_company_name = choice(list(remaining)).name
    newpath = reverse('detail', args=(new_company_name,))
    print newpath
    return HttpResponseRedirect(newpath)


def _render(request, templatename, variables):
    context = RequestContext(request, variables)
    template = loader.get_template(templatename)
    return HttpResponse(template.render(context))


def thankyou(request):
    voter_id = _voter(request)
    voter = Voter.objects.get(id=voter_id)
    return _render(request, 'noname/thankyou.html', {'voter': voter})


def next(request):
    voter_id = _voter(request)
    voter = Voter.objects.get(id=voter_id)
    return _next(voter)


def detail(request, pk):
    voter_id = _voter(request)
    voter = Voter.objects.get(id=voter_id)
    companyname = get_object_or_404(CompanyName, pk=pk)
    voter.pages_seen.add(companyname)

    if not request.POST:
        voterform = VoterForm(instance=voter)
    else:
        voterform = VoterForm(request.POST, instance=voter)

    if request.POST and voterform.is_valid():
        voter.optional_nickname = voterform.cleaned_data['optional_nickname']
        voter.optional_email = voterform.cleaned_data['optional_email']
        voter.optional_info = voterform.cleaned_data['optional_info']
        voter.save()

    evalform = EvaluationForm(request.POST)
    if evalform.is_valid():
        evaluation = Evaluation()
        evaluation.author = voter
        evaluation.subject = companyname
        evaluation.eval_date = date.today()

        evaluation.value = evalform.cleaned_data['value']
        evaluation.message = evalform.cleaned_data['message']

        evaluation.save()

        voter.pages_voted.add(companyname)
        return _next(voter)

    if request.POST:
        # Here, the user posted some data but the evalform wasn't valid (see
        # above) so we display erros. See also EvaluationForm.custom_display.
        evalform.display_errors = True
    else:
        # Here, the user didn't post any data so it's the first time he sees the
        # page: we don't display errors.
        evalform.display_errors = False

    variables = {
        'companyname': companyname,
        'voter': voter,
        'evalform': evalform,
        'voterform': voterform,
    }
    return _render(request, 'noname/detail.html', variables)


def index(request):
    voter_id = _voter(request)
    voter = Voter.objects.get(id=voter_id)
    variables = {
        'voter': voter,
        'all_proposed_names': CompanyName.objects.all(),
        }
    return _render(request, 'noname/index.html', variables)
