from datetime import date, datetime
from random import choice

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from noname.forms import EvaluationForm, VoterForm
from noname.models import CompanyName, Voter

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


def _first_in_iterable(collection):
    return collection.__iter__.next()

def _otherthan(voter, lastseen, voted=False):
    allcomp = CompanyName.objects.all()

    remaining = frozenset(allcomp) \
        - frozenset(voter.pages_seen.all()) \
        - frozenset((lastseen,))

    if not remaining:
        remaining = frozenset(allcomp) - frozenset(voter.pages_voted.all())
        if not remaining:
            if voted:
                #Congrats, you've been voting for all items
                return HttpResponseRedirect("/noname/thankyou/")

    remaining_nb = len(remaining)
    if remaining_nb == 0:
        base = frozenset(allcomp) - frozenset((lastseen,))
        if not base:
            new_company_name = _first_in_iterable(remaining)
        else:
            new_company_name = choice(tuple(base))
    elif remaining_nb == 1:
        new_company_name = _first_in_iterable(remaining)
    else:
        #a relative path. We are 'appname/next'
        new_company_name = choice(tuple(remaining))
    newpath = reverse('detail', args=(new_company_name.name,))
    return HttpResponseRedirect(newpath)


def _render(request, templatename, variables):
    context = RequestContext(request, variables)
    template = loader.get_template(templatename)
    return HttpResponse(template.render(context))


def thankyou(request):
    voter = _voter(request)
    return _render(request, 'noname/thankyou.html', {'voter': voter})


def otherthan(request, name=''):
    voter = _voter(request)
    try:
        name = CompanyName.objects.get(name=name)
    except CompanyName.DoesNotExist:
        name = None
    return _otherthan(voter, name)


def _saveforms(request, forms):
    """
    Saves if applicable, and yields True or False if saved.
    Does NOT commit to DB.
    """
    if not request.POST:
        for form in forms:
            yield False
        return

    for form in forms:
        try:
            form.save(commit=False)
        except ValueError:
            form.display_errors = True
            yield False
        else:
            yield True

def detail(request, pk):
    voter = _voter(request)
    companyname = get_object_or_404(CompanyName, pk=pk)
    voter.pages_seen.add(companyname)
    evaluation = voter.get_evaluation(companyname)

    #seems request.POST can be None safely
    evalform = EvaluationForm(request.POST, instance=evaluation)
    voterform = VoterForm(request.POST, instance=voter)

    forms = evalform, voterform

    #Does NOT commit to DB.
    eval_data, voter_data = _saveforms(request, forms)

    voterform.save(commit=False)

    #info that was not supplied in forms
    if eval_data:
        evalform.save(commit=False)
        if evaluation.value == '':
            evaluation.value = -1

        #manually tweak evaluation
        evaluation.author = voter
        evaluation.subject = companyname
        evaluation.date_of_modification = date.today()

        #manually tweak voter
        voter.pages_voted.add(companyname)
        #And now we commit to db

        #voting is done, let's go to next page
        voterform.save_m2m()
        evalform.save_m2m()
        #BUG: save_m2m should have saved, but the eval is not in db unless this:
        evaluation.save()
        return _otherthan(voter, companyname, voted=True)

    voterform.save()

    if request.POST:
        # Here, the user posted some data but the evalform wasn't valid (see
        # above) so we display erros. See also EvaluationForm.custom_display.
        for form in forms:
            form.display_errors = True
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
