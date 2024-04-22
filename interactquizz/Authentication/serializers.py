from rest_framework import serializers
from .models import CustomUser
# from main.serializers import LevelSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    level = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        return user

    def get_level(self, obj):
        return obj.level
