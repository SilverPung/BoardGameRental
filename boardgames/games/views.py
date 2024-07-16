from django.shortcuts import render, redirect
from .forms import GameForm
# Create your views here.


def add_game(request, event_id):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save(event_id = event_id) 
            return redirect('core:event_detail',event_id)
    else:
        form = GameForm()
    return render(request, 'games/add_game.html', {'form': form})