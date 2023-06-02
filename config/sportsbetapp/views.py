from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.theoddsapi import get_sports, get_upcoming_games
from .models import Game





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

#api 'getsports' to test api connection
def sports(request):
    api_key = "cff6cb1b3c6773cdd7053a1f54b84342"
    sports = get_sports(api_key)
    context = {
        "sports": sports,
    }
    return render(request, "sports.html", context)

# this displays events stored as Game in models
def home(request):
    get_upcoming_games()
    upcoming_games = Game.objects.all() # or filter based on your requirements
    return render(request, 'home.html', {'games': upcoming_games})

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    outcomes = game.outcomes.all()

    context = {
        'game': game,
        'outcomes': outcomes,
    }
    return render(request, 'game_detail.html', context)