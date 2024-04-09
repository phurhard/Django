from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'age', 'username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            age=validated_data.get('age'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email')
        )
        return user

# "success": true,
#   "message": "User created successfully",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMjc0MDIzNywiaWF0IjoxNzEyNjUzODM3LCJqdGkiOiJlNzg2MTZmYmIzMDU0MGRlYmQ4ODI5ZjQ1Yzk5MzEwNiIsInVzZXJfaWQiOjF9.ZBpKVJp6wuAvovrydxmLqVc3udog68BrR6t1cBuvG1w",
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNjU0MTM3LCJpYXQiOjE3MTI2NTM4MzcsImp0aSI6IjE0NTY4OTEwZGViZDQ0MGFhOTI0ZDc5NWQyMWY1OGQ1IiwidXNlcl9pZCI6MX0.ft8rmrJcNFOZVhkeq9KRK2MtpSZw6jJzB_c1Ig_225I"