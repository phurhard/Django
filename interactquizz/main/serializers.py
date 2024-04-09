from dataclasses import field
from rest_framework import serializers
from Authentication.models import Question, Answer, Level, Subject, CustomUser
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
    subject_name = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['level'] = LevelSerializer(instance.level).data
        representation['subject_name'] = SubjectSerializer(instance.subject_name).data
        return representation


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Answer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['question'] = QuestionSerializer(instance.question).data
        representation['user'] = UserSerializer(instance.user).data
        return representation
