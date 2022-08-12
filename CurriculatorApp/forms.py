from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Column, Fieldset, Layout, Row, HTML


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['username']
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class ProfiloForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['sesso']
        fields = [
            'data_nascita',
            'luogo_nascita',
            'foto',
            'telefono',
        ]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Registrati'))


class SezioneForm(forms.ModelForm):
    class Meta:
        model = Sezione
        fields = ['titolo', 'curriculum']

    def __init__(self, *args, **kwargs):
        curriculum_default = kwargs.pop('curriculum', None)
        super(SezioneForm, self).__init__(*args, **kwargs)
        self.fields['curriculum'].disabled = True


SezioneFormSet = modelformset_factory(Sezione, form=SezioneForm, extra=1, fields=['titolo', 'curriculum'])

#SezioneFormSet = modelformset_factory(
#    Sezione, fields=("titolo", "curriculum"), extra=1
#)


