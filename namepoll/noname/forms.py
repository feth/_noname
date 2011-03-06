from django.forms import ModelForm, RadioSelect

from .models import Evaluation, Voter

class EvaluationForm(ModelForm):
    class Meta(object):
        model = Evaluation
        fields = ('value', 'message')
        widgets = {
            'value': RadioSelect
            }

class VoterForm(ModelForm):
    class Meta(object):
        model = Voter
        exclude = ('pages_seen',)

