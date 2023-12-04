from rest_framework import serializers

from master_system.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "body", "user", "is_synced")
        model = Post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "body", "user", "is_synced")
        model = Post

    def update(self, instance, validated_data):
        instance.is_synced = False
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "email", "body", "postId", "is_synced")
        model = Comment


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "email", "body", "postId", "is_synced")
        model = Comment

    def update(self, instance, validated_data):
        instance.is_synced = False
        return super().update(instance, validated_data)
