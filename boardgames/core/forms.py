from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description']
     
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)