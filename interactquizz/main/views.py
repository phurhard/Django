from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    SubjectSerializer,
    LevelSerializer,
    UserSerializer
    )
from Authentication.models import Question, Answer, Subject, Level, CustomUser

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return None
        return UserSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """The view for the questions
    will need to edit this to allow for query parameters
    so users can request for question in a specific leveland a specific subject"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get query parameters from the request
        level = self.request.query_params.get('level', None)
        subject = self.request.query_params.get('subject', None)

        # Filter queryset based on parameters
        if level is not None:
            queryset = queryset.filter(level__name=level)
        if subject is not None:
            queryset = queryset.filter(subject_name__name=subject)

        return queryset


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
