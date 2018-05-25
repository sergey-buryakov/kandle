from django import forms


class CreateEventForm(forms.Form):
    name = forms.CharField(label="Название")
    description = forms.CharField(label="Описание", widget=forms.Textarea)