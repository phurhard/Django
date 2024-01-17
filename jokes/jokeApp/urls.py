from django.urls import path
from . import views

urlpatterns = [
    path('joker/', views.jokes, name='joke'),
    path('server/', views.requestJoke, name='requestJoke'),
]
