from django.urls import path, include
from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet, LevelViewSet, SubjectViewSet

router = routers.DefaultRouter()

router.register(r'level', LevelViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api_auth/', include('rest_framework.urls')),
]
