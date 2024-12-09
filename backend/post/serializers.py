from rest_framework import serializers

from backend.account.serializers import UserSerializer
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_ago', 'likes_count', 'is_liked', 'comments_count', )
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'created_at', )