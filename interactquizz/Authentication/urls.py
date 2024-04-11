from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', UserViewSet.as_view({'post': 'create'}), name='Signup'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='Login'),
]

# urlpatterns += router.urls
