from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
# from main.serializers import LevelSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    level = serializers.SerializerMethodField()
    age = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])

    class Meta:
        model = CustomUser
        fields = ["username", "password", "first_name", "last_name", "age", "level"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        print(password)
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    @extend_schema_field(serializers.IntegerField())
    def get_level(self, obj):
        return obj.level


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
