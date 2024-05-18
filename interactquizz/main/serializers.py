from rest_framework import serializers
from Authentication.models import (
    Option, Question, Answer, Level, Quiz, Score, Subject, CustomUser)
from Authentication.serializers import UserSerializer


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all())
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['level'] = LevelSerializer(instance.level).data
        representation['subject_name'] = SubjectSerializer(
            instance.subject).data
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


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.email

    def get_quiz(self, obj):
        return obj.quiz.title


class QuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"
