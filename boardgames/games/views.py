from django.shortcuts import render, redirect
from .forms import GameForm, RentalForm
from core.models import Game
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

def edit_game(request, game_id):
    game = Game.objects.get(id=game_id)
    form = GameForm(instance=game)
    rental_form = RentalForm()
    if request.method == 'POST':
        form_type = request.POST.get('form_type', None)
        if form_type == 'rental':
            rental_form = RentalForm(request.POST)
            if rental_form.is_valid():
                game.add_renter(rental_form.cleaned_data['barcode'])
                game.accessible -= 1
                game.save(event_id=game.event.id)
                return redirect('core:event_detail',game.event.id)
        elif form_type == 'edit_game':
            form = GameForm(request.POST, instance=game)
            if form.is_valid():
                form.save()
                return redirect('core:event_detail',game.event.id)
    return render(request, 'games/edit_game.html', {'form': form, 'game': game,'rental_form':rental_form})