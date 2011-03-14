from datetime import date, datetime
from functools import wraps
from random import choice

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader

from noname.forms import EvaluationForm, VoterForm
from noname.models import CompanyName, Voter

SESSIONS_EXPIRY = datetime(2011, 12, 31, 23, 59, 59, 999)


def _voter(request):
    """
    does a bunch of things with the request to have a decent voter.
    """
    if "voter" in request.session:
        return request.session["voter"], False

    #### Once per session

    #set expiration date
    request.session.set_expiry(SESSIONS_EXPIRY)
    #ensure there is a container for seen names
    request.session.setdefault("seen", [])
    #make a default voter
    voter = Voter()
    voter.save() #so it's guaranteed to have an id
    request.session["voter"] = voter

    return voter, True


def logout(request):
    """
    Does not use @usevoter on purpose: we don't want a voter object created!
    """
    if 'voter' in request.session:
        del request.session['voter']
    return HttpResponseRedirect(reverse('index'))


def usevoter(view):
    """
    Decorator for view that use a 'voter' as their first argument
    If no voter existed before, it calls 'welcome'
    """
    @wraps(view)
    def replacement(request, *args, **kwargs):
        voter, created = _voter(request)
        if not created:
            return view(voter, request, *args, **kwargs)
        return HttpResponseRedirect(reverse('welcome'))

    return replacement


def _render(request, templatename, variables):
    context = RequestContext(request, variables)
    template = loader.get_template(templatename)
    return HttpResponse(template.render(context))


class OtherThan(object):

    def __init__(self, voter, allcomp=None):

        self.voter = voter

        if allcomp is None:
            allcomp = CompanyName.objects.all()
        self.allcomp = frozenset(allcomp)

    def _remainingpages(self):
        """
        Pages not seen or not voted yet
        """
        result = self.allcomp - frozenset(self.voter.pages_seen.all())
        if result:
            return result
        return self.allcomp - frozenset(self.voter.companies_voted)


    def _redir2companyname(self, companyname):
        newpath = reverse('detail', args=(companyname.name,))
        return HttpResponseRedirect(newpath)


    def _choosenext(self, lastseen, remaining=None):
        if remaining is None:
            remaining = self.allcomp
        choices = remaining - frozenset((lastseen,))

        if not choices:
            return self._redir2companyname(lastseen)

        return self._redir2companyname(choice(tuple(choices)))


    def next(self, lastseen, voted=False):
        remaining = self._remainingpages()

        if remaining:
            return self._choosenext(lastseen, remaining=remaining)

        if voted:
            #Congrats, you've been voting for all items
            return HttpResponseRedirect("/noname/thankyou/")

        return self._choosenext(lastseen)


@usevoter
def thankyou(voter, request):
    return _render(request, 'noname/thankyou.html', {'voter': voter})


@usevoter
def otherthan(voter, request, name=''):
    try:
        name = CompanyName.objects.get(name=name)
    except CompanyName.DoesNotExist:
        name = None
    other = OtherThan(voter)
    return other.next(name)


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


@usevoter
def eval(voter, request, pk):
    #FIXME: XXX XXX XXX
    #check value: must be int. Seems django will fix it otherwise.
    #FIXME: XXX XXX XXX
    #XSS
    companyname = get_object_or_404(CompanyName, pk=pk)
    evaluation = voter.get_evaluation(companyname)
    evaluation.value = request.POST['value']
    evaluation.save()
    voter.save()
    return _render(request, 'noname/valideval.html', {})


@usevoter
def message(voter, request, pk):
    #FIXME: XXX XXX XXX
    #XSS
    companyname = get_object_or_404(CompanyName, pk=pk)
    evaluation = voter.get_evaluation(companyname)
    evaluation.message = request.POST['message']
    evaluation.save()
    voter.save()
    return _render(request, 'noname/valideval.html', {})


@usevoter
def voterinfo(voter, request):
    print "voterinfo XXX TODO: parse request.POST"
    print request.POST
    voter.optional_nickname = request.POST['nickname']
    voter.optional_email = request.POST['email']
    voter.optional_info = request.POST['info']
    voter.save()
    return _render(request, 'noname/valideval.html', {})


@usevoter
def detail(voter, request, pk):
    companyname = get_object_or_404(CompanyName, pk=pk)
    voter.pages_seen.add(companyname)
    evaluation = voter.get_evaluation(companyname)

    if not request.POST:
        # If this isn't a POST request, we don't use it to fill the form
        evalform = EvaluationForm(instance=evaluation)
    else:
        evalform = EvaluationForm(request.POST, instance=evaluation)
        voterform = VoterForm(request.POST, instance=voter)

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
        evaluation.date_of_modification = date.today()

        #voting is done, let's go to next page
        voterform.save_m2m()
        evalform.save_m2m()
        #BUG: save_m2m should have saved, but the eval is not in db unless this:
        evaluation.save()
        other = OtherThan(voter)
        return other.next(companyname, voted=True)

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


@usevoter
def index(voter, request):
    variables = {
        'voter': voter,
        'all_proposed_names': CompanyName.objects.all(),
        }
    return _render(request, 'noname/index.html', variables)

def welcome(request):
    return render_to_response('noname/welcome.html')
