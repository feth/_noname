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
        # XXX: This is a dirty method to display the form as we would want.
        # It should be changed anytime soon.
        return mark_safe(u"""
<p>
    <label for="id_value_0">What do you think this name would be to our company?</label>
<div id=blah>
    <label for="id_value_0">
        <input value="0" type="radio" class="star" name="value" id="id_value_0" />
        Prejudiciable
    </label>
    <label for="id_value_1">
        <input value="1" type="radio" class="star" name="value" id="id_value_1" />
        Valid
    </label>
    <label for="id_value_2">
        <input value="2" type="radio" class="star" name="value" id="id_value_2" />
        Great
    </label>
</div>
</p>

<p>
    <label for="id_message">Message:</label>
</p>
<p>
    <textarea id="id_message" rows="10" cols="40" name="message"></textarea>
</p>""")


class VoterForm(ModelForm):
    class Meta(object):
        model = Voter
        exclude = ('pages_seen', 'pages_voted')

    def custom_display(self):
        # XXX: This is a dirty method to display the form as we would want.
        # It should be changed anytime soon.
        return mark_safe(u"""
<p>
    <label for="id_optional_nickname">Optional nickname:</label>
    <input id="id_optional_nickname" type="text" name="optional_nickname" maxlength="100" />
</p>

<p>
    <label for="id_optional_email">Optional email:</label>
    <input id="id_optional_email" type="text" name="optional_email" maxlength="100" />
</p>
<p>
    <label for="id_optional_info">Optional info:</label>
</p>
<p>
    <textarea id="id_optional_info" rows="10" cols="40" name="optional_info"></textarea>
</p>
""")
