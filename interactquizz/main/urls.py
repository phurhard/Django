from django.urls import path, include
from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, LevelViewSet, SubjectViewSet
from Authentication.views import UserViewSet

router = routers.DefaultRouter()

router.register(r'level', LevelViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api_auth/', include('rest_framework.urls')),
    # path('signup/', UserViewSet.as_view({'post': 'create'}), name='Signup'),
    # path('login/', UserViewSet.as_view({'post': 'login'}), name='Login'),
]
