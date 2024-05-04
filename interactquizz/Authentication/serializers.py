from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework_simplejwt.tokens import RefreshToken


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
    # level = serializers.SerializerMethodField()
    # age = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     # print(password)
    #     user = CustomUser.objects.create(**validated_data, age=10)
    #     user.set_password(password)
    #     # user.age = 10
    #     user.save()
    #     return user

    # @extend_schema_field(serializers.IntegerField())
    # def get_level(self, obj):
        # return obj.level


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
