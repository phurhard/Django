from django.urls import path
from .views import (
    UserLogin, UserSignup, RefreshTokenView, AdminSignup)


urlpatterns = [
    path('admin/signup/', AdminSignup.as_view(), name='admin-signup'),
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
]
