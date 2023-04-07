from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User


# Create your views here.
def members(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    # If the user is already logged in, redirect to the home page
    if request.user.is_authenticated:
        return redirect('home')

    # If this is a POST request, process the login form data
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    # Render the login template with the form
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