from django.forms import ModelForm, RadioSelect
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

from .models import Evaluation, Voter

class MyRFRenderer(RadioFieldRenderer):
    def render(self):
        return mark_safe(
            u'<div id=blah>\n%s</div>\n' % u'\n'.join([u'%s'% force_unicode(w) for w in self]) + u'\n'
            )

class EvaluationForm(ModelForm):
    class Meta(object):
        model = Evaluation
        fields = ('value', 'message')
        widgets = {
            'value': RadioSelect(attrs={'class':'star'}, renderer=MyRFRenderer)
            }

class VoterForm(ModelForm):
    class Meta(object):
        model = Voter
        exclude = ('pages_seen', 'pages_voted')

