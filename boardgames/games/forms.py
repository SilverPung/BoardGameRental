from django import forms
from core.models import Game

login_atributes = 'form-control rounded-xl py-3 w-full bg-gray-300'

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'barcode', 'distributor', 'description', 'quantity', 'bgg_url', 'image']

    bgg_url = forms.URLField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'bgg_url'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Tytuł'}))
    barcode = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Kod kreskowy'}))
    distributor = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder':'Wydawca'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Opis'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Ilość sztuk'}))
    image = forms.ImageField(widget=forms.TextInput(attrs={'class': login_atributes, 'placeholder': 'Zdjęcie'}))
