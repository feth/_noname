from datetime import date, datetime
from random import choice

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from noname.forms import EvaluationForm, VoterForm
from noname.models import CompanyName, Evaluation, Voter

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
    return HttpResponseRedirect(newpath)


def _render(request, templatename, variables):
    context = RequestContext(request, variables)
    template = loader.get_template(templatename)
    return HttpResponse(template.render(context))


def thankyou(request):
    voter = _voter(request)
    return _render(request, 'noname/thankyou.html', {'voter': voter})


def next(request):
    voter = _voter(request)
    return _next(voter)


def _eval_and_form(voter, companyname, request):

    evaluations_tuple = voter.evaluations.filter(subject=companyname)
    evaluation = evaluations_tuple[0] if evaluations_tuple else None
    form_kwarg = {'instance': evaluation} if evaluation else {}

    if request.POST:
        return evaluation, EvaluationForm(request.POST, **form_kwarg)

    return evaluation, EvaluationForm(**form_kwarg)


def _valid_evaluation(voter, companyname, form, evaluation):
    """
    form is valid.
    evaluation may be None.
    this function saves voter
    """
    if evaluation is None:
        evaluation = Evaluation()

    evaluation.author = voter
    evaluation.subject = companyname
    evaluation.eval_date = date.today()
    evaluation.value = form.cleaned_data['value']
    evaluation.message = form.cleaned_data['message']
    evaluation.save()

    voter.pages_voted.add(companyname)
    voter.save()

    return _next(voter)


def _update_voter(voter, form):
    """
    form is valid
    function does NOT save voter.
    """
    voter.optional_nickname = form.cleaned_data['optional_nickname']
    voter.optional_email = form.cleaned_data['optional_email']
    voter.optional_info = form.cleaned_data['optional_info']


def detail(request, pk):
    voter = _voter(request)
    companyname = get_object_or_404(CompanyName, pk=pk)
    voter.pages_seen.add(companyname)

    if not request.POST:
        voterform = VoterForm(instance=voter)
    else:
        voterform = VoterForm(request.POST, instance=voter)

    update_voter = request.POST and voterform.is_valid()
    if update_voter:
        _update_voter(voter, voterform)

    evaluation, evalform = _eval_and_form(voter, companyname, request)

    if request.POST:
        if evalform.is_valid():
            return _valid_evaluation(voter, companyname, evalform, evaluation)
        # Here, the user posted some data but the evalform wasn't valid (see
        # above) so we display erros. See also EvaluationForm.custom_display.
        evalform.display_errors = True
    else:
        # Here, the user didn't post any data so it's the first time he sees the
        # page: we don't display errors.
        evalform.display_errors = False

    if update_voter:
        voter.save()

    variables = {
        'companyname': companyname,
        'voter': voter,
        'evalform': evalform,
        'voterform': voterform,
    }
    return _render(request, 'noname/detail.html', variables)


def results(request):
    results = (
        (companyname,) + companyname.normscore()
        for companyname in CompanyName.objects.all()
        )

    variables = {
        'results': results
    }
    return _render(request, 'noname/results.html', variables)


def index(request):
    voter = _voter(request)
    variables = {
        'voter': voter,
        'all_proposed_names': CompanyName.objects.all(),
        }
    return _render(request, 'noname/index.html', variables)
