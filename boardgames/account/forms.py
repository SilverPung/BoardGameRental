from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


login_atributes = 'form-control rounded-xl py-3 w-full bg-gray-300'



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
    username = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Nazwa Użytkownika'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': login_atributes, 'placeholder': 'Email'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': login_atributes,
            'placeholder': 'Obecne Hasło',
        })
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': login_atributes,
            'placeholder': 'Nowe Hasło',
        })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': login_atributes,
            'placeholder': 'Potwierdź Nowe Hasło',
        })