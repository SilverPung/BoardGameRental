from django.test import TestCase
from .forms import GameForm, RentalForm, RatingForm
from core.models import Game


class GameFormTest(TestCase):
    def test_game_form(self):
        form = GameForm(data={
            'barcode': '1234567890',
            'title': 'Game1',
            'distributor': 'Distributor1',
            'quantity': 10,
            'description': 'Description1'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('barcode'), '1234567890')
        self.assertEqual(form.cleaned_data.get('title'), 'Game1')
        self.assertEqual(form.cleaned_data.get('distributor'), 'Distributor1')
        self.assertEqual(form.cleaned_data.get('quantity'), 10)
        self.assertEqual(form.cleaned_data.get('description'), 'Description1')
    def test_saving_game_form(self):
        form = GameForm(data={
            'barcode': '1234567890',
            'title': 'Game1',
            'distributor': 'Distributor1',
            'quantity': 10,
            'description': 'Description1'
        })
        self.assertTrue(form.is_valid())
        game = form.save()
        self.assertEqual(game.barcode, '1234567890')
        self.assertEqual(game.title, 'Game1')
        self.assertEqual(game.distributor, 'Distributor1')
        self.assertEqual(game.quantity, 10)
        self.assertEqual(game.description, 'Description1')

