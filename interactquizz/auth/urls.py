from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('refresh-token/', refresh_jwt_token),
]
