from django.urls import path, include
from rest_framework import routers
from .views import (
    QuestionViewSet,
    AnswerViewSet,
    LevelViewSet,
    SubjectViewSet,
    UserViewSet
    )

router = routers.DefaultRouter()

router.register(r'level', LevelViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
