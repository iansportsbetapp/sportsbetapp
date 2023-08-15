from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView



urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mydashboard/', views.Mydashboard, name='mydashboard'),
    path('game/<str:game_id>/', views.game_detail, name='game_detail'),
    # URL pattern for serving the sports.json file
    path('api/sports.json', TemplateView.as_view(template_name='/Users/ian/sportsbetapp/config/api/sports.json'), name='sports_json'),
    path('get_upcoming_games/<str:selected_sport>/', views.get_upcoming_games, name='get_upcoming_games'),
    path('<str:selected_sport>/', views.home, name='home'),
]