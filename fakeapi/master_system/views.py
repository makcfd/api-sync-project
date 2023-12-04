from rest_framework import viewsets
from master_system.models import Post, Comment
from master_system.serializers import (
    PostSerializer,
    PostUpdateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return PostUpdateSerializer
        return PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return CommentUpdateSerializer
        return CommentSerializer
