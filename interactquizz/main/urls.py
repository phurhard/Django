from django.urls import path, include
from rest_framework import routers

from .views import (
    AnswerViewDetail,
    AnswerViewList,
    QuestionViewList,
    QuestionViewDetail,)

urlpatterns = [
    path('question/', QuestionViewList.as_view(), name='questions-create'),
    path('answer/', AnswerViewList.as_view(), name='answer-create'),
    path('question/<int:id>/', QuestionViewDetail.as_view(),
         name='questions-detail'),
    path('answer/<int:id>/', AnswerViewDetail.as_view(),
         name='answer-detail'),
]
