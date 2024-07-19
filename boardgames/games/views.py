from django.shortcuts import render, redirect
from .forms import GameForm, RentalForm, RatingForm
from core.models import Game, Event, Renter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
LIMIT_OF_RENTED_GAMES = 2 #limit of games that can be rented by one user
@login_required
def add_game(request, event_id):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game=form.save(commit=False)
            game.event=Event.objects.get(id=event_id)
            game.save()
            return redirect('core:event_detail',event_id)
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = GameForm()
    return render(request, 'games/add_game.html', {'form': form})


@login_required
def edit_game(request, game_id):
    game = Game.objects.get(id=game_id)
    form = GameForm(instance=game)  
    rental_form = RentalForm()  
    rating_form = RatingForm()
    list_of_renters = game.list_of_renters.all()  
    if request.method == 'POST':
        form_type = request.POST.get('form_type', None)
        
        if form_type == 'rental':#renting game
            rental_form = RentalForm(request.POST)

            if rental_form.is_valid():
                renters_barcode=rental_form.cleaned_data['barcode']
                try:
                    can_be_rented = Renter.objects.get(barcode=renters_barcode).how_many_games>=LIMIT_OF_RENTED_GAMES
                except Renter.DoesNotExist:
                    can_be_rented = False
                if renters_barcode in list_of_renters.values_list('barcode', flat=True) or can_be_rented:
                    messages.error(request, 'Gra jest już wypożyczona lub osoba wypożyczająca ma już maksymalną ilość gier.')
                else:
                    game.add_renter(renters_barcode)
                    game.accessible -= 1
                    game.save()
                    renter = Renter.objects.get(barcode=renters_barcode)
                    renter.how_many_games+=1
                    renter.save()
                    messages.success(request, 'Gra została wypożyczona.')
                
                return redirect('core:event_detail', game.event.id)
            
            else:
                print(rental_form.errors)

        elif form_type == 'edit_game':  # editing game
            form = GameForm(request.POST,request.FILES, instance=game)
            if form.is_valid():
                form.save()
                messages.success(request, 'Gra została zaktualizowana.')
                return redirect('core:event_detail', game.event.id)
            else:
                messages.error(request, form.errors)
                print(form.errors)

        if 'renter_id' in request.POST:#removing renter
            renter_id = request.POST.get('renter_id', None)
            renter = game.list_of_renters.get(id=renter_id)
            renter.how_many_games-=1
            renter.save()
            game.list_of_renters.remove(renter)
            game.accessible += 1
            game.save()
            rating=RatingForm(request.POST)
            if rating.is_valid() and int(rating.cleaned_data['rating'])>0:
                rating=rating.cleaned_data['rating']
                game.avg_rating=(game.avg_rating*game.rating_count+int(rating))/(game.rating_count+1)
                game.rating_count+=1
                game.save()
            messages.success(request, 'Gra została zwrócona.')
            return redirect('core:event_detail', game.event.id)
    context={'form': form, 'game': game, 'rental_form': rental_form, 'list_of_renters': list_of_renters, 'rating_form': rating_form}
    return render(request, 'games/edit_game.html',context)