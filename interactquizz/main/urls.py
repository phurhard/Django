from django.urls import path, include
from rest_framework import routers
from .views import (
    AnswerViewDetail,
    AnswerViewList,
    OptionView,
    QuestionViewList,
    QuestionViewDetail,
    QuizView,
    QuizViewDetail,
    ScoreViewDetail,
    ScoreViewList,
    submit_quiz,
    user_result
    )

urlpatterns = [
    path('question/', QuestionViewList.as_view(), name='questions-create'),
    path('answer/', AnswerViewList.as_view(), name='answer-create'),
    path('question/<int:id>/', QuestionViewDetail.as_view(),
         name='questions-detail'),
    path('answer/<int:id>/', AnswerViewDetail.as_view(),
         name='answer-detail'),
    # path('score/', ScoreViewList.as_view(), name='score-create'),
    path('answer/<int:id>', AnswerViewDetail.as_view(), name='score-detail'),
    path('quiz/', QuizView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/', QuizViewDetail.as_view(), name='quiz-detail'),
    path('option/', OptionView.as_view(), name='options'),
    path('score/', submit_quiz, name='scores'),
    path('results/', user_result, name='results'),
]
