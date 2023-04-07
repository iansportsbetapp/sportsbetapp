from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),


]