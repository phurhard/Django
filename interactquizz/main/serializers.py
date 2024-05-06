from rest_framework import serializers
from Authentication.models import (
    Option, Question, Answer, Level, Quiz, QuizSet, Score, Subject, CustomUser)
from Authentication.serializers import UserSerializer


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())
    subject_name = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all())

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['level'] = LevelSerializer(instance.level).data
        representation['subject_name'] = SubjectSerializer(
            instance.subject_name).data
        return representation


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = Answer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['question'] = QuestionSerializer(instance.question).data
        representation['user'] = UserSerializer(instance.user).data
        return representation


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuizSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSet
        fields = "__all__"
