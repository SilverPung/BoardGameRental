from django import forms
from core.models import Game

atributes = 'form-control rounded-xl py-3 w-full bg-gray-300'

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'barcode', 'distributor', 'description', 'quantity', 'image','accessible']

    title = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Tytuł'}))
    barcode = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Kod kreskowy'}))
    distributor = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder':'Wydawca'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded-xl py-6 w-full bg-gray-300', 'placeholder': 'Opis'}),required=False)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': atributes, 'placeholder': 'Ilość sztuk'}),initial=1,min_value=1)
    accessible = forms.IntegerField(widget=forms.NumberInput(attrs={'class': atributes, 'placeholder': 'Dostępne sztuki'}),initial=1,min_value=1)
    image = forms.ImageField(widget=forms.FileInput(attrs={ 'placeholder': 'Zdjęcie'}),required=False)

    def save(self, commit=True, event_id=None):
        game_instance = super(GameForm, self).save(commit=False)
        if commit:
            game_instance.save(event_id=event_id)
        return game_instance
class BggForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded-l py-3 px-48 w-full bg-gray-300', 'placeholder': 'Wyszukaj'}))


class RentalForm(forms.Form):
    barcode = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Kod kreskowy wypożyczającego'}))
