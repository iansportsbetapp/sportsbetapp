from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('members/', views.members, name='members'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mydashboard/', views.Mydashboard, name='mydashboard'),
]