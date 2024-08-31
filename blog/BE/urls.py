from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<str:pk>', views.post, name='post'),
]