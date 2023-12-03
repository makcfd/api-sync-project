from multiprocessing import synchronize
from rest_framework import serializers

from master_system.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "body")
        model = Post


# TODO: change mixin for this serializer
class PostUpdateSerializer(serializers.ModelSerializer):
    synch_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ("id", "title", "body", "user")
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "email", "body")
        model = Comment
