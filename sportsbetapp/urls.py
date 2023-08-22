from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('game/<str:game_id>/', views.game_detail, name='game_detail'),
    path('sports_with_games/', views.sports_with_games, name='sports_with_games'),  # New URL for fetching sports data from the database
    path('get_upcoming_games/<str:selected_sport>/', views.get_upcoming_games, name='get_upcoming_games'),
    path('<str:selected_sport>/', views.home, name='home_with_sport'),
]