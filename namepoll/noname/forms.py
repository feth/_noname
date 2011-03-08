#-*-coding:utf-8-*-
from django.forms import ModelForm, RadioSelect
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

from .models import Evaluation, Voter

class EvaluationForm(ModelForm):
    """
    Model for the evalutation form
    """
    class Meta(object):
        model = Evaluation
        fields = ("value", 'message',)
        widgets = {
            'value': RadioSelect(attrs={'class':'star'})
            }

    def custom_display(self):
        if hasattr(self, "display_errors") and not self.display_errors:
            normal_row = u'<p%(html_class_attr)s><b>%(label)s</b> <br/> %(field)s%(help_text)s</p><br/>'
        else:
            normal_row = u'<p%(html_class_attr)s><b>%(label)s</b> <br/> %(field)s%(help_text)s<font color="ForestGreen">%(errors)s</font></p>'

        return self._html_output(
            normal_row = normal_row,
            error_row = u'',
            row_ender = '</p><br/>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)


class VoterForm(ModelForm):
    class Meta(object):
        model = Voter
        exclude = ('pages_seen', 'pages_voted', 'weight')

    def custom_display(self):
        return self._html_output(
            normal_row = u'<p%(html_class_attr)s><b>%(label)s</b> <br/> %(field)s%(help_text)s<font color="ForestGreen">%(errors)s</font></p>',
            error_row = u'%s',
            row_ender = '</p>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)
