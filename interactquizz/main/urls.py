from django.urls import path, include
from .views import (
    QuizView,
    submit_quiz,
    user_result,
    view_corrections,
    create_question,
    addQuiz,
    get_questions
    )

urlpatterns = [
    path('quiz/', QuizView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/', get_questions, name='quiz-detail'),
    path('submit_quiz/', submit_quiz, name='scores'),
    path('results/<int:quiz_id>/', user_result, name='results'),
    path('corrections/<quiz_id>/', view_corrections, name='view-corrections'),
    path('create-question/', create_question, name='create-question'),
    path('add-quiz/', addQuiz, name='add-quiz'),
]
