from django import forms
from core.models import Game, Event
from django.core.exceptions import ValidationError
import requests
from django.core.files.base import ContentFile
from boardgamegeek import BGGClient


atributes = 'form-control rounded-xl py-3 w-full bg-gray-300 pl-2'


class GameForm(forms.ModelForm):
    image_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL Zdjęcia'}))

    class Meta:
        model = Game
        fields = ['title', 'barcode', 'distributor', 'description', 'event', 'quantity', 'image', 'accessible', 'top', 'image_url','min_players', 'max_players', 'min_playtime', 'max_playtime', 'categories', 'mechanics']

    title = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Tytuł'}))
    barcode = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Kod kreskowy'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded-xl py-6 w-full bg-gray-300', 'placeholder': 'Opis'}), required=False)
    distributor = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Dystrybutor'}), required=False)
    event = forms.ModelChoiceField(required=False, queryset=Event.objects.all(), widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': atributes, 'placeholder': 'Ilość sztuk'}), initial=1, min_value=1)
    accessible = forms.IntegerField(widget=forms.NumberInput(attrs={'class': atributes, 'placeholder': 'Dostępne sztuki'}), initial=1, min_value=1, required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Zdjęcie'}), required=False)
    top = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    bgg_id = forms.CharField(widget=forms.HiddenInput(), required=False)


    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode')
        if Game.objects.filter(barcode=barcode).exists() and not self.instance:
            raise ValidationError("Istnieje już gra z takim kodem kreskowym", code='unique')
        return barcode

    def clean(self):
        cleaned_data = super().clean()
        image_url = cleaned_data.get('image_url')

        if image_url and not cleaned_data.get('image'):
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                image_name = image_url.split('/')[-1]
                cleaned_data['image'] = ContentFile(response.content, image_name)
            except requests.exceptions.RequestException:
                raise ValidationError("Nie można pobrać obrazu z podanego URL.")
        
        return cleaned_data
    
    def save(self):
        game = super().save()
        if self.cleaned_data.get('bgg_id'):
            bgg = BGGClient()
            game.bgg_id = self.cleaned_data.get('bgg_id')
            bgg_game = bgg.game(game_id=game.bgg_id)
            game.min_players = bgg_game.min_players
            game.max_players = bgg_game.max_players
            game.min_playtime = bgg_game.min_playing_time
            game.max_playtime = bgg_game.max_playing_time
            game.categories = ';'.join(bgg_game.categories)
            game.mechanics = ';'.join(bgg_game.mechanics)
            game.save()
        return game


class BggForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded-l py-3 px-48 w-full bg-gray-300', 'placeholder': 'Wyszukaj'}))


class RentalForm(forms.Form):
    barcode = forms.CharField(widget=forms.TextInput(attrs={'class': atributes, 'placeholder': 'Kod kreskowy wypożyczającego'}))

class RatingForm(forms.Form):
    RATING_CHOICES = [(i, str(i)) for i in range(11)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': atributes, 'placeholder': 'Ocena'}))  