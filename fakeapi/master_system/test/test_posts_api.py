from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from ..models import Post

User = get_user_model()


class PostsAPITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        """Fixtures for the tests."""
        super().setUpClass()
        OBJECT_ID = 1
        cls.url_list = reverse("posts-list")
        cls.url_detail = reverse(
            "posts-detail",
            kwargs={"pk": OBJECT_ID},
        )

        cls.bulk_list = list()
        for i in range(3):
            cls.bulk_list.append(
                Post(
                    title=f"Title {i}",
                    body=f"Description of post {i}",
                )
            )
        Post.objects.bulk_create(cls.bulk_list)

        cls.data = {"title": "Amazing post", "body": "Something about post"}
        cls.new_data = {"title": "Update is ready", "body": "Let's update it"}

    def setUp(self):
        self.user = User.objects.create_user(
            username="johnsnow",
            email="johnsnow@johnsnow.me",
            password="johnsnowpassword",
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

        self.num_posts_init = Post.objects.all().count()

    def test_get_posts_list_no_auth(self):
        """Getting 401 if not authenticated."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_posts_list(self):
        """Correct status and number of posts retrived."""
        num_posts_init = Post.objects.all().count()
        response = self.client.get(self.url_list)
        num_post_resp = len(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(num_post_resp, num_posts_init)

    def test_post_new_posts_auth(self):
        """New post created correctly."""
        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), self.data.get("title"))
        self.assertEqual(response.data.get("body"), self.data.get("body"))
        self.assertEqual(response.data.get("user"), settings.DEFAULT_USER_ID)

    def test_post_new_posts_no_auth(self):
        """Unautheticated attempt of post creation fails."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detailed_after_post_auth(self):
        """Succusfully retrive object after calling POST."""
        post_response = self.client.post(self.url_list, self.data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        post_id = post_response.data["id"]
        detail_url = reverse("posts-detail", kwargs={"pk": post_id})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post_auth(self):
        """Successfully delete post authenticated."""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_no_auth(self):
        """Fail to delete post unauthenticated."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partially_update_post_auth(self):
        """A post title patched correctly."""
        data = {"title": "Patch is ready"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), data.get("title"))

    def test_partially_update_post_no_auth(self):
        """An unauthenticated post patch fails."""
        self.client.force_authenticate(user=None, token=None)
        data = {"title": "Patch is ready"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_post_update_auth(self):
        """A post updated correctly."""
        response = self.client.put(self.url_detail, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("title"),
            self.new_data.get("title"),
        )
        self.assertEqual(response.data.get("body"), self.new_data.get("body"))

    def test_full_post_update_no_auth(self):
        """An unauthenticated post update fails."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(self.url_detail, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
