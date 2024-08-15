from django.shortcuts import render, redirect
from .forms import GameForm, RentalForm, RatingForm
from core.models import Game, Event, Renter, KnownDistributor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from boardgamegeek import BGGClient
from django.views.generic import TemplateView

# Create your views here.
LIMIT_OF_RENTED_GAMES = 2  # limit of games that can be rented by one user


@login_required
def add_game(request, event_id):
    form = GameForm()
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            game = form.save()
            game.event = Event.objects.get(id=event_id)
            game.save()
            messages.success(request, "Gra została dodana pomyślnie.")
            return redirect("core:event_detail", event_id)
        else:
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = GameForm()
    return render(request, "games/add_game.html", {"form": form, "event_id": event_id})


@login_required
def edit_game(request, game_id):
    game = Game.objects.get(id=game_id)
    form = GameForm(instance=game)
    rental_form = RentalForm()
    rating_form = RatingForm()
    list_of_renters = game.list_of_renters.all()

    if request.method == "POST":
        form_type = request.POST.get("form_type", None)

        if form_type == "delete_game":  # Deleting game
            event_id = game.event.id
            game.delete()
            messages.success(request, "Gra została usunięta.")
            return redirect("core:event_detail", event_id)

        elif form_type == "rental":  # Renting game
            rental_form = RentalForm(request.POST)
            if rental_form.is_valid():
                renters_barcode = rental_form.cleaned_data["barcode"]
                try:
                    can_be_rented = (
                        Renter.objects.get(barcode=renters_barcode).how_many_games
                        >= LIMIT_OF_RENTED_GAMES
                    )
                except Renter.DoesNotExist:
                    can_be_rented = False
                if (
                    renters_barcode in list_of_renters.values_list("barcode", flat=True)
                    or can_be_rented
                ):
                    messages.error(
                        request,
                        "Gra jest już wypożyczona lub osoba wypożyczająca ma już maksymalną ilość gier.",
                    )
                else:
                    game.add_renter(renters_barcode)
                    game.save()
                    messages.success(request, "Gra została wypożyczona.")
                return redirect("core:event_detail", game.event.id)
            else:
                print(rental_form.errors)

        elif form_type == "edit_game":  # Editing game
            form = GameForm(request.POST, request.FILES, instance=game)
            if form.is_valid():
                form.save()
                messages.success(request, "Gra została zaktualizowana.")
                return redirect("core:event_detail", game.event.id)
            else:
                messages.error(request, form.errors)
                print(form.errors)

        elif "renter_id" in request.POST:  # Removing renter
            renter_id = request.POST.get("renter_id", None)
            renter = game.list_of_renters.get(id=renter_id)
            renter.how_many_games -= 1
            renter.save()
            game.list_of_renters.remove(renter)
            game.accessible += 1
            game.save()
            rating = RatingForm(request.POST)
            if rating.is_valid() and int(rating.cleaned_data["rating"]) > 0:
                rating = rating.cleaned_data["rating"]
                game.add_rating(rating)
            messages.success(request, "Gra została zwrócona.")
            return redirect("core:event_detail", game.event.id)

    context = {
        "form": form,
        "game": game,
        "rental_form": rental_form,
        "list_of_renters": list_of_renters,
        "rating_form": rating_form,
    }
    return render(request, "games/edit_game.html", context)


def fetch_bgg_data(request):
    if request.method == "GET":
        bgg_url = request.GET.get("bgg_url")
        if bgg_url:
            bgg_id = bgg_url.split("/")[-2]
            bgg = BGGClient()
            game = bgg.game(game_id=bgg_id)
            names = game.alternative_names if game.alternative_names else []
            names.insert(0, game.name)
            data = {
                "image": game._image,
                "distributors": game.publishers if game.publishers else [],
                "titles": names,
                "bgg_id": bgg_id,

            }
            return JsonResponse(data)

        return JsonResponse({"error": "BGG URL is required"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_distributor_suggestions(request):
    event_id = request.GET.get("event_id")
    # Fetch suggestions based on the query (replace with your actual data fetching logic)
    suggestions = KnownDistributor.objects.filter(
        event=Event.objects.get(id=event_id)
    ).values_list("distributor", flat=True)

    return JsonResponse(suggestions, safe=False)
