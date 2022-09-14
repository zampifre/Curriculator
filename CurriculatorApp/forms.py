from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory, DateInput

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Column, Fieldset, Layout, Row, HTML, Field


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
        self.fields['curriculum'].widget = forms.HiddenInput()
        self.fields['curriculum'].disabled = True
        self.fields['titolo'].help_text = "La sezione verrà aggiunta al CV"


SezioneFormSet = modelformset_factory(Sezione, form=SezioneForm, extra=1, fields=['titolo', 'curriculum'])

#SezioneFormSet = modelformset_factory(
#    Sezione, fields=("titolo", "curriculum"), extra=1
#)

class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['titolo', 'data_inizio', 'data_fine', 'sezione', 'campi']

    def __init__(self, sezione, *args,  **kwargs):
        self.sezione = sezione
        super(ElementoForm, self).__init__(*args, **kwargs)
        self.fields['sezione'].queryset = self.sezione
        self.fields['campi'].help_text = "Inserisci ogni voce tra le virgolette, separa i campi con ':'"
        #self.fields['sezione'].widget = forms.HiddenInput()
        #self.fields['sezione'].disabled = True


ElementoFormSet = modelformset_factory(Elemento, form=ElementoForm, extra=1,
                                       fields=['titolo', 'data_inizio', 'data_fine', 'sezione', 'campi'])


class ElementForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = {'titolo', 'data_inizio', 'data_fine', 'campi'}
        widgets = {
            'data_inizio': DateInput(attrs={'type': 'date'}),
            'data_fine': DateInput(attrs={'type': 'date'})
        }
        exclude = {'sezione'}
