from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
##members view - THIS CAN BE DELETED
def members(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

from django.shortcuts import render

##homepage view
def home(request):
    return render(request, 'home.html')

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