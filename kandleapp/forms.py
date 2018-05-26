from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class Sign_up_form(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CreateEventForm(forms.Form):
    name = forms.CharField(label="Название")
    description = forms.CharField(label="Описание", widget=forms.Textarea)