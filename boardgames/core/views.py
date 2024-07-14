from django.shortcuts import render
from .models import Event
#from .forms import EventForm
# Create your views here.


def home(request):
    events = Event.objects.all()

    return render(request, 'core/home.html', {'events': events})