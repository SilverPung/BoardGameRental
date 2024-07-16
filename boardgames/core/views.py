from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event, Game
from .forms import EventForm, LoginForm, SignupForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q  # Import Q

@login_required
def home(request):
    events = Event.objects.filter(allowed_users__in=[request.user])
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event=form.save(user=request.user)  # Save the form to the database
            return redirect('core:event_detail',new_event.id)  # Redirect to the home view
    else:
        form = EventForm()  # Instantiate a new form for a GET request
    
    return render(request, 'core/home.html', {'events': events, 'form': form})

@login_required
@login_required
def event_detail(request, event_id):
    action = request.GET.get('action')
    iterator = int(request.GET.get('iterator', 0))  # Default to 0 if not provided

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
    # Calculate the slice indices based on the iterator
    start_index = iterator * 5
    end_index = start_index + 5
    top_games = games.order_by('title')[start_index:end_index]
    max_iterator = games.count() // 5
    return render(request, 'core/event_detail.html', {'event': event, 'form': form, 'top_games': top_games, 'iterator': iterator, 'max_iterator': max_iterator})