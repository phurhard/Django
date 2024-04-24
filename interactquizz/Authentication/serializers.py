from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework_simplejwt.tokens import RefreshToken
# from main.serializers import LevelSerializer


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')
        try:
            token = RefreshToken(refresh_token)
            token.verify()
        except Exception as e:
            # print(e) log this
            raise serializers.ValidationError('Invalid refresh token')

        return attrs


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
