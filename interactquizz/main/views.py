from django.shortcuts import render
from rest_framework import viewsets
from .serializers import QuestionSerializer, AnswerSerializer, SubjectSerializer, LevelSerializer
from Authentication.models import Question, Answer, Subject, Level, CustomUser
from Authentication.serializers import UserSerializer
# Create your views here.


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
