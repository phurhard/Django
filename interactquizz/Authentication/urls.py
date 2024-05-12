from django.contrib import admin
from django.urls import path
from .views import (
    ProfileUser, UserLogin, UserSignup, RefreshTokenView, AdminSignup)


urlpatterns = [
    path('admin/signup/', AdminSignup.as_view(), name='admin-signup'),
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('profile/', ProfileUser.as_view(), name='profile'),
]
