from django.shortcuts import render, redirect
from .models import Event, Game
from .forms import EventForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q 

@login_required
def home(request):
    events = Event.objects.filter(allowed_users__in=[request.user])
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event=form.save(user=request.user)
            return redirect('core:event_detail',new_event.id) 
    else:
        form = EventForm()  
    
    return render(request, 'core/home.html', {'events': events, 'form': form})

@login_required
def event_detail(request, event_id):
    action = request.GET.get('action')
    iterator = int(request.GET.get('iterator', 0)) 

    if action == 'increment':
        iterator += 1
    elif action == 'decrement':
        iterator -= 1

    event = Event.objects.get(id=event_id)
    games = Game.objects.filter(event=event)
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            games = Game.objects.filter(
                Q(title__icontains=query) | Q(barcode__icontains=query),
                event=event
            )
    start_index = iterator * 5
    end_index = start_index + 5
    top_games = games.order_by('title')[start_index:end_index]
    max_iterator = games.count() // 5
    return render(request, 'core/event_detail.html', {'event': event, 'form': form,
                                                      'top_games': top_games, 
                                                      'iterator': iterator, 
                                                      'max_iterator': max_iterator})


@login_required
def logout(request):
    return render(request, 'core/logout.html')# todo: implement logout view


def summary(request,event_id):
    Number_of_games=10
    if Game.objects.filter(event=event_id).count()<3:
        return redirect('core:event_detail',event_id)
    if Game.objects.filter(event=event_id).count()<10:
        Number_of_games=Game.objects.filter(event=event_id).count()
    games=Game.objects.filter(event=event_id).order_by('-avg_rating','-rating_count')[:Number_of_games]
    top_game=games[0]
    second_game=games[1]
    third_game=games[2]
    games=games[3:]
    context={'top_game':top_game,'second_game':second_game,'third_game':third_game,'games':games}
    return render(request, 'core/summary.html',context=context)


