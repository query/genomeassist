from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms

from .models import Job


login_helper = FormHelper()
login_helper.form_action = 'login'
login_helper.form_class = 'form form-horizontal'
login_helper.label_class = 'col-lg-2'
login_helper.field_class = 'col-lg-10'
login_helper.layout = Layout(
    'username',
    Field('password', css_class='form-control'),
    Div(
        FormActions(
            Submit('submit', 'Log in', css_class='btn btn-primary'),
            css_class='col-lg-offset-2 col-lg-10'
        ),
        css_class='form-group'
    )
)



class JobForm(forms.ModelForm):
    class Meta(object):
        model = Job
        fields = ['name', 'read', 'reference', 'options']

    helper = FormHelper()
    helper.form_action = 'scheduler:create'
    helper.form_class = 'form form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = Layout(
        'name',
        'read',
        'reference',
        'options',
        Div(
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary'),
                css_class='col-lg-offset-2 col-lg-10'
            ),
            css_class='form-group'
        )
    )
