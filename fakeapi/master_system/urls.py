from rest_framework.routers import DefaultRouter
from django.urls import include, path

from master_system.views import PostViewSet, CommentViewSet

router = DefaultRouter()

router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("v1/", include(router.urls)),
]
