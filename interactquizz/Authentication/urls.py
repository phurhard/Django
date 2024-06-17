from django.urls import path
from .views import (
    UserLogin, UserSignup, RefreshTokenView,
    logout_view, profile_view,
    quiz_view, home_view
    )


urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('quiz/', quiz_view, name='quiz'),
    path('home/', home_view, name='home'),
]
