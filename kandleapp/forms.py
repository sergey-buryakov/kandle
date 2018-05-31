from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Event
from django.contrib.admin import widgets

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
        }
