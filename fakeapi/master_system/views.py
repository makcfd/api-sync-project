from requests import Session

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from master_system.models import Post
from master_system.serializers import PostSerializer, PostUpdateSerializer

# TODO make this url as const in setting file
jsonplaceholder_url = "https://jsonplaceholder.typicode.com/posts"


def synch_with_jsonplaceholder(data):
    # data = {"title": "Text_Max", "body": "BOD_Test", "userId": 1}

    s = Session()
    # TODO add try and catch
    resp = s.request(method="POST", url=jsonplaceholder_url, data=data)
    print(f"Synch STATUS: {resp.status_code}")


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return PostUpdateSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # synch_with_jsonplaceholder(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_update(self, serializer):
        serializer.save()
        # synch_with_jsonplaceholder(serializer.data)

    # with create there is no synch

    # make synch for PUT and PATCH
