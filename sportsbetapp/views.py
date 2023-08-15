from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse, request
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Game
import json
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.conf import settings
from django.templatetags.static import static
import os





# Create your views here.
##members view - THIS CAN BE DELETED
def members(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

from django.shortcuts import render

##homepage view - this may be deleted
# def home(request):
#     return render(request, 'home.html')

#login form
def login_view(request):
    # If the user is already logged in, redirect to the home page
    if request.user.is_authenticated:
        return redirect('home')

    # If this is a POST request, process the login form data
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('mydashboard')
    else:
        form = AuthenticationForm()

    # Render the login template with the form
    return render(request, 'login.html', {'form': form})

#register/signup form
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

#Dashboard view
def Mydashboard(request):
    template = loader.get_template('mydashboard.html')
    return HttpResponse(template.render())

# this displays events stored as Game in models
def home(request, selected_sport=None):
    # Construct the path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'sportsbetapp', 'sports.json')
    with open(json_file_path, 'r') as file:
        sports_data = json.load(file)
    
    active_sports = [sport['description'] for sport in sports_data if sport['active']]

    # We don't need to do anything special with selected_sport here
    # as the selection is handled on the frontend by the JavaScript code

    context = {
    'active_sports': [{'key': sport['key'], 'description': sport['description']} for sport in sports_data if sport['active']],
}
    
    return render(request, 'home.html', context)

def get_upcoming_games(request, selected_sport):
    print("Decoded selected_sport: ", selected_sport)

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Check for 'undefined' values and convert to datetime if valid
    start_date = make_aware(datetime.strptime(start_date_str, '%Y-%m-%d')) if start_date_str != 'undefined' else None
    end_date = make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')) if end_date_str != 'undefined' else None

    try:
        # Filter based on start_date and end_date if they exist
        if start_date and end_date:
            games = Game.objects.filter(sport_key=selected_sport, commence_time__range=[start_date, end_date]).values()
        else:
            games = Game.objects.filter(sport_key=selected_sport).values()
        
        games_list = list(games)
        for game in games_list:
            if isinstance(game.get('commence_time'), datetime):
                game['commence_time'] = game['commence_time'].isoformat()
        print(json.dumps(games_list, indent=4)) 
    except ObjectDoesNotExist:
        games_list = []  # No games found for the given sport_key

    return JsonResponse(games_list, safe=False)

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    outcomes = game.outcome_set.all()

    context = {
        'game': game,
        'outcomes': outcomes,
    }
    return render(request, 'game_detail.html', context)