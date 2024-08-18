from django import forms
from .models import Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


login_atributes = 'form-control rounded-xl py-3 w-full bg-gray-300'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description']
     
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    add_default_users = forms.BooleanField(required=False, initial=True)
    


    def save(self, commit=True,user=None):

        event_instance = super(EventForm, self).save(commit=False)
        
        if commit:
            event_instance.save()  
            if self.cleaned_data.get('add_default_users'):
 
                event_instance.add_default_users()
            event_instance.add_logged_in_user(user)
                
        return event_instance


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Nazwa Użytkownika'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': login_atributes, 'placeholder': 'Hasło'}))


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Nazwa Użytkownika'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': login_atributes, 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': login_atributes, 'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': login_atributes, 'placeholder': 'Potwierdź Hasło'}))
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded-l py-3 px-48 w-full bg-gray-300', 'placeholder': 'Wyszukaj'}),required=False, label='' ,initial='')


class SimilarityForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control rounded-xl py-3 w-full bg-gray-300', 'placeholder': 'Opis gry której szukamy'}),required=False, label='Opis')