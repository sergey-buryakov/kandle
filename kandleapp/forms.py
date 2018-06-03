from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Event, Date
from django.utils.translation import ugettext_lazy as _

# class DateInput(forms.DateInput):
#     input_type = 'date'

class Sign_up_form(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'startVote', 'finishVote']
        widgets = {
            'name': forms.TextInput(),
            'startVote': forms.DateInput(attrs={'class': 'input-sm form-control'}),
            'finishVote': forms.DateInput(attrs={'class': 'input-sm form-control'})
        }
        labels = {
            'name': _('Название'),
            'description': _('Описание')
        }
class CreateDate(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['date', 'startTime', 'finishTime']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'startTime': forms.DateInput(attrs={'class':'timepicker'}),
            'finishTime': forms.DateInput(attrs={'class':'timepicker'})
        }
