from rest_framework.serializers import ModelSerializer
from .models import CustomUser, UserPost
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class CustomUserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)


class UserPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['caption', 'content']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return UserPost.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        return {
            'user': user,
        }

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'is_staff', 'is_superuser'] 
    