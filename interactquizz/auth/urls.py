from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('token-auth/', TokenObtainPairView.as_view(), name='token_auth_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
]
