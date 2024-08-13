from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    is_follower = serializers.SerializerMethodField()
    sent_request = serializers.SerializerMethodField()
    received_request = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'bio', 'followers', 'following', 'is_following', 'is_follower', 'sent_request', 'received_request')
    
    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        user = self.context.get('request').user
        return user.following.filter(pk=obj.pk).exists()

    def get_is_follower(self, obj):
        user = self.context.get('request').user
        return obj.followers.filter(pk=user.pk).exists()

    def get_sent_request(self, obj):
        user = self.context.get('request').user
        return user.sent_requests.filter(to_user=obj.pk).exists()

    def get_received_request(self, obj):
        user = self.context.get('request').user
        return user.received_requests.filter(from_user=obj.pk).exists()
