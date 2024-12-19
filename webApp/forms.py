from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django import forms
from webApp.models import *

class  ChefRegistrationForm(UserCreationForm): 

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(ChefRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))


class  AdminAddressForm(forms.ModelForm): 

    class Meta:
        model = AdminAddress
        fields =   ['address_details']
        # fields =   ['address_line1','address_line2','city','country','postal_code']


    def __init__(self, *args, **kwargs):
        super(AdminAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
