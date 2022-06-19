from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Meme, Like


class MemeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Meme
        fields = ['id', 'photo', 'author', 'likes', 'created_at']

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = []
