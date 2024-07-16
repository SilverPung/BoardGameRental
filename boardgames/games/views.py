from django.shortcuts import render
from .forms import GameForm
# Create your views here.


def add_game(request, event_id):
    form = GameForm()
    return render(request, 'games/add_game.html', {'form': form})