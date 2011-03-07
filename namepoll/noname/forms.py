from django.forms import ModelForm, RadioSelect
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

from .models import Evaluation, Voter

class MyRFRenderer(RadioFieldRenderer):
    """
    Custom rendering for the RadioSelect: We need them side to side.
    Default rendering makes <ul><li>
    """
    def render(self):
        return mark_safe(
            u'<div id="rating">\n%s\n</div><!-- end #rating -->\n' % u'\n'.join([u'%s'% force_unicode(w) for w in self])
            )

class EvaluationForm(ModelForm):
    class Meta(object):
        model = Evaluation
        fields = ('value', 'message')
        widgets = {
            'value': RadioSelect(attrs={'class':'star'}, renderer=MyRFRenderer)
            }

    def custom_display(self):
        return self._html_output(
            normal_row = u'<p%(html_class_attr)s><b>%(label)s</b> <br/> %(field)s%(help_text)s</p>',
            error_row = u'%s',
            row_ender = '</p>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)


class VoterForm(ModelForm):
    class Meta(object):
        model = Voter
        exclude = ('pages_seen', 'pages_voted')

    def custom_display(self):
        return self._html_output(
            normal_row = u'<p%(html_class_attr)s><b>%(label)s</b> <br/> %(field)s%(help_text)s</p>',
            error_row = u'%s',
            row_ender = '</p>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)
