from django.shortcuts import render, redirect
from .forms import GameForm, RentalForm
from core.models import Game, Event
# Create your views here.


def add_game(request, event_id):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game=form.save(commit=False)
            game.event=Event.objects.get(id=event_id)
            game.save()
            return redirect('core:event_detail',event_id)
        else:
            print(form.errors)
    else:
        form = GameForm()
    return render(request, 'games/add_game.html', {'form': form})

def edit_game(request, game_id):
    game = Game.objects.get(id=game_id)
    # Assuming game is defined earlier in the view
    form = GameForm(instance=game)  # Initialize outside of POST block for GET requests
    rental_form = RentalForm()  # Initialize outside of POST block for GET requests
    list_of_renters = game.list_of_renters.all()  # Assuming this is how you get the list of renters

    if request.method == 'POST':
        form_type = request.POST.get('form_type', None)
        if form_type == 'rental':
            rental_form = RentalForm(request.POST)
            if rental_form.is_valid():
                renters_barcode=rental_form.cleaned_data['barcode']
                if renters_barcode in list_of_renters.values_list('barcode', flat=True):
                    pass
                else:
                    game.add_renter(renter)
                    game.accessible -= 1
                    game.save()
                return redirect('core:event_detail', game.event.id)
            else:
                print(rental_form.errors)
        elif form_type == 'edit_game':
            form = GameForm(request.POST, instance=game)
            if form.is_valid():
                form.save()
                return redirect('core:event_detail', game.event.id)
            else:
                print(form.errors)  # Corrected to form.errors
        if 'renter_id' in request.POST:
            renter_id = request.POST.get('renter_id', None)
            renter = game.list_of_renters.get(id=renter_id)
            game.list_of_renters.remove(renter)
            game.accessible += 1
            game.save()
            return redirect('core:event_detail', game.event.id)

    return render(request, 'games/edit_game.html', {'form': form, 'game': game, 'rental_form': rental_form, 'list_of_renters': list_of_renters})