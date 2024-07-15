from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event
from .forms import EventForm, LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

@login_required
def home(request):
    events = Event.objects.all()
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
    event=Event.objects.get(id=event_id)
    return render(request, 'core/event_detail.html', {'event': event})

        