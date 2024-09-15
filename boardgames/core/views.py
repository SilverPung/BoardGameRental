
from django.shortcuts import render, redirect
from .models import Event, Game
from .forms import EventForm, SearchForm, SignupForm, SimilarityForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.contrib.auth import logout
from rest_framework import generics
from .serializers import GameSerializer
import requests
from django.contrib import messages
from django.conf import settings



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
    top = request.GET.get('top')
    min_players = request.GET.get('min_players')
    max_players = request.GET.get('max_players')
    min_playtime = request.GET.get('min_playtime')
    max_playtime = request.GET.get('max_playtime')
    iterator = int(request.GET.get('iterator', 0)) 
    reset = request.GET.get('reset')

    if action == 'increment':
        iterator += 1
    elif action == 'decrement':
        iterator -= 1


    

    event = Event.objects.get(id=event_id)
    games = Game.objects.filter(event=event)
    form = SearchForm()
    similarityform = SimilarityForm()
    if reset == 'true':
        min_players = None
        max_players = None
        min_playtime = None
        max_playtime = None
        top = False
    else:
        if top == 'true':
            games=games.filter(top=True)
        if min_players:
            games=games.filter(Q(max_players__gte=int(min_players) )| Q(max_players__isnull=True))
        if max_players:
            games=games.filter(Q(min_players__lte=int(max_players)) | Q(min_players__isnull=True))
        if min_playtime:
            games=games.filter(Q(min_playtime__gte=int(min_playtime)) | Q(max_playtime__isnull=True))
        if max_playtime:
            games=games.filter(Q(max_playtime__lte=int(max_playtime)) | Q(min_playtime__isnull=True))
    
    

    if request.method == 'POST':
        form_type = request.POST.get("form_type", None)
        if form_type == 'search':
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                games = games.filter(
                    Q(title__icontains=query) | Q(barcode__icontains=query),
                    event=event 
                )
                iterator = 0
            else:
                games = games.filter(event=event)
        elif form_type == 'similarity':
            
            similarityform = SimilarityForm(request.POST)
            
            
            if similarityform.is_valid():
                print(similarityform.cleaned_data)
                
                payload = similarityform.cleaned_data 
                payload.update({'event_id': event_id})
                try:
                    
                    response = requests.post('http://127.0.0.1:5000/boardgames/similarity/', json=payload)
                    if response.status_code == 200:
                        pass
                    else:
                        pass
                except requests.exceptions.RequestException as e:
                    messages.error(request, 'Wystąpił błąd podczas łączenia z serwerem.')
                    return render(request, 'core/event_detail.html', {'event': event, 'form': form, 'similarityform': similarityform})
    start_index = iterator * 5
    end_index = start_index + 5
    top_games = games.order_by('title')[start_index:end_index]
    max_iterator = (games.count()-1) // 5
    context={'event': event, 'form': form, 'top_games': top_games, 'iterator': iterator, 
             'max_iterator': max_iterator, 'similarity_form': similarityform, 'beta': settings.BETA, 
             'min_players': min_players, 'max_players': max_players, 'min_playtime': min_playtime, 
             'max_playtime': max_playtime, 'top': top}
    return render(request, 'core/event_detail.html', context=context)

@login_required
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


@login_required
def logout_view(request):
    
    if request.method == 'POST':
        logout(request)
        return redirect('core:home')
    
    return render(request, 'core/logout.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def custom_page_not_found(request, exception):
    return render(request, 'core/404.html', status=404)


class GameListView(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Game.objects.filter(event=event_id)
    
