from rest_framework import serializers

from master_system.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "body",
            "user",
        )
        model = Post


class PostUpdateSerializer(serializers.ModelSerializer):
    is_synced = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "title", "body", "user", "is_synced")
        model = Post

    def get_is_synced(self, instance):
        return getattr(instance, "is_synced", None)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "email", "body", "postId")
        model = Comment

    def get_is_synced(self, instance):
        return getattr(instance, "is_synced", None)


class CommentUpdateSerializer(serializers.ModelSerializer):
    is_synced = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name", "email", "body", "postId", "is_synced")
        model = Comment

    def get_is_synced(self, instance):
        return getattr(instance, "is_synced", None)
