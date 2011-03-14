#coding: utf-8
from django.forms import ModelForm, RadioSelect

from .models import Evaluation, Voter


class EvaluationForm(ModelForm):
    """
    Model for the evaluation form
    """
    class Meta(object):
        model = Evaluation
        fields = ("value", 'message',)
        widgets = {
            'value': RadioSelect(attrs={'class':'star'})
            }


class VoterForm(ModelForm):
    class Meta(object):
        model = Voter
        exclude = ('pages_seen', 'weight')

    def custom_display(self):
        return self._html_output(
            normal_row = u'<p%(html_class_attr)s><b>%(label)s</b> <br/> %(field)s%(help_text)s<font color="ForestGreen">%(errors)s</font></p>',
            error_row = u'%s',
            row_ender = '</p>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)

