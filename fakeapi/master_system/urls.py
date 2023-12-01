from rest_framework.routers import SimpleRouter
from django.urls import include, path

from master_system.views import PostViewSet

router = SimpleRouter()

router.register("api/v1/posts", PostViewSet, basename="posts")
router.register("api/v1/posts/<int:pk>", PostViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
