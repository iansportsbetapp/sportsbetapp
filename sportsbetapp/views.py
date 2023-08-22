from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Game, Sport
import json
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.conf import settings
import os
from django.db.models import Count, Q


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('mydashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def my_dashboard(request):
    return render(request, 'mydashboard.html')


def home(request, selected_sport=None):
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'sportsbetapp', 'sports.json')
    with open(json_file_path, 'r') as file:
        sports_data = json.load(file)
    
    context = {
        'active_sports': [{'key': sport['key'], 'description': sport['description']} for sport in sports_data if sport['active']],
    }
    
    return render(request, 'home.html', context)


def get_upcoming_games(request, selected_sport):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_date = make_aware(datetime.strptime(start_date_str, '%Y-%m-%d')) if start_date_str != 'undefined' else None
    end_date = make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')) if end_date_str != 'undefined' else None

    try:
        if start_date and end_date:
            games = Game.objects.filter(sport__key=selected_sport, commence_time__range=[start_date, end_date]).values()

        else:
            games = Game.objects.filter(sport__key=selected_sport).values()
        
        games_list = list(games)
        for game in games_list:
            if isinstance(game.get('commence_time'), datetime):
                game['commence_time'] = game['commence_time'].isoformat()
    except ObjectDoesNotExist:
        games_list = []

    return JsonResponse(games_list, safe=False)


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    outcomes = game.outcome_set.all()

    context = {
        'game': game,
        'outcomes': outcomes,
    }
    return render(request, 'game_detail.html', context)

def sports_with_games(request):
    print("Entered sports_with_games view")
    # Get dates from request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    print('start_date_str', start_date_str, 'end_date_str', end_date_str)

    # Convert the dates to datetime objects (if they are valid)
    start_date = make_aware(datetime.strptime(start_date_str, '%Y-%m-%d')) if start_date_str else None
    end_date = make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')) if end_date_str else None

    #Testing error: empty list returned
    print("Before setting start_date:", start_date_str)
    print("After setting start_date:", start_date)
    
    # Ensure the start date is less than or equal to the end date
    if not start_date or not end_date or start_date > end_date:
        return JsonResponse([], safe=False)  # Return an empty list

    # Get the sports that have games within the specified date range
    sports = Sport.objects.annotate(
        num_games=Count('games', filter=Q(games__commence_time__range=[start_date, end_date]))
    ).filter(num_games__gt=0).values('key', 'title', 'is_active')
    
    print(sports.query)

    return JsonResponse(list(sports), safe=False)


