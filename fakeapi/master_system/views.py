from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from master_system.models import Post, Comment
from master_system.serializers import (
    PostSerializer,
    PostUpdateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)
from master_system.utility import synchronize_to_external_api


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        is_synced = synchronize_to_external_api("post", instance, created=True)
        instance.is_synced = is_synced

    def perform_update(self, serializer):
        instance = serializer.save()
        is_synced = synchronize_to_external_api("post", instance, created=False)
        instance.is_synced = is_synced

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_synced = synchronize_to_external_api("post", instance, delete=True)

        if is_synced:
            self.perform_destroy(instance)
            return Response(
                {"is_synced": is_synced},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "Synchronization failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostUpdateSerializer
        return PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        is_synced = synchronize_to_external_api("comment", instance, created=True)
        instance.is_synced = is_synced

    def perform_update(self, serializer):
        instance = serializer.save()
        is_synced = synchronize_to_external_api("comment", instance, created=False)
        instance.is_synced = is_synced

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_synced = synchronize_to_external_api("comment", instance, delete=True)

        if is_synced:
            self.perform_destroy(instance)
            return Response(
                {"is_synced": is_synced},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "Synchronization failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentUpdateSerializer
        return CommentSerializer
