from django.urls import path, include
from rest_framework import routers

from .views import (
    AnswerViewDetail,
    AnswerViewList,
    OptionView,
    QuestionViewList,
    QuestionViewDetail,
    QuizSetView,
    QuizView,
    ScoreViewDetail,
    ScoreViewList,)

urlpatterns = [
    path('question/', QuestionViewList.as_view(), name='questions-create'),
    path('answer/', AnswerViewList.as_view(), name='answer-create'),
    path('question/<int:id>/', QuestionViewDetail.as_view(),
         name='questions-detail'),
    path('answer/<int:id>/', AnswerViewDetail.as_view(),
         name='answer-detail'),
    path('score/', ScoreViewList.as_view(), name='score-create'),
    path('answer/<int:id>', AnswerViewDetail.as_view(), name='score-detail'),
    path('quiz/', QuizView.as_view(), name='quiz-create'),
    path('quizset/', QuizSetView.as_view(), name='quizset'),
    path('option/', OptionView.as_view(), name='options'),
]
