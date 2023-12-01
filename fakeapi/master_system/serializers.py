from rest_framework import serializers

from master_system.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "body", "user")
        model = Post
