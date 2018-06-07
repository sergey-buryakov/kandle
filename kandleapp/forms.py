from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Event, Date
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class Sign_up_form(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        
        fields = ['name', 'description', 'startVote', 'finishVote', 'private']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'startVote': forms.DateInput(attrs={'class': 'input-sm form-control'}),
            'finishVote': forms.DateInput(attrs={'class': 'input-sm form-control'})
        }
        labels = {
            'name': _('Title'),
            'description': _('Description')
        }
class CreateDate(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['date', 'startTime', 'finishTime']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker form-control date_in'}),
            'startTime': forms.DateInput(attrs={'class':'timepicker form-control'}),
            'finishTime': forms.DateInput(attrs={'class':'timepicker form-control'})
        }

