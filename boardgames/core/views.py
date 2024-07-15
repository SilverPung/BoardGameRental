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
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    games = Game.objects.filter(event=event)
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Filter by title or barcode
            games = Game.objects.filter(
                Q(title__icontains=query) | Q(barcode__icontains=query),
                event=event  # Ensure to also filter by event
            )
    top_games = games.order_by('title')[:5]
    return render(request, 'core/event_detail.html', {'event': event, 'form': form, 'top_games': top_games})

