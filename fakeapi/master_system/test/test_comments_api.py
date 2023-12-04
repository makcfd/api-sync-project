from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Comment, Post

User = get_user_model()


class CommentsAPITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        """Fixtures for the tests."""
        super().setUpClass()
        OBJECT_ID = 1
        cls.url_list = reverse("comments-list")
        cls.url_detail = reverse(
            "comments-detail",
            kwargs={"pk": OBJECT_ID},
        )
        post = Post.objects.create(
            title="Super test post",
            body="Full body",
        )
        cls.bulk_list = list()
        for i in range(3):
            cls.bulk_list.append(
                Comment(
                    name=f"Name {i}",
                    email=f"email{i}@email.email",
                    body=f"Description of comment {i}",
                    postId=post,
                )
            )
        Comment.objects.bulk_create(cls.bulk_list)
        cls.data = {
            "name": "Amazing comment",
            "body": "Something about comment",
            "email": "new@new.new",
            "postId": 1,
        }
        cls.new_data = {
            "name": "Update is ready",
            "body": "Let's update it",
            "email": "updated@email.com",
            "postId": 1,
        }

    def setUp(self):
        # TODO: reuse the user
        self.user = User.objects.create_user(
            username="johnsnow",
            email="johnsnow@johnsnow.me",
            password="johnsnowpassword",
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

        self.num_comment_init = Comment.objects.all().count()

    def test_get_comments_list_no_auth(self):
        """Getting 401 if not authenticated."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_list(self):
        """Correct status and number of comments retrived."""
        num_posts_init = Comment.objects.all().count()
        response = self.client.get(self.url_list)
        num_post_resp = len(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(num_post_resp, num_posts_init)

    def test_post_new_comments_auth(self):
        """New comment created correctly."""
        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), self.data.get("name"))
        self.assertEqual(response.data.get("body"), self.data.get("body"))
        self.assertEqual(response.data.get("email"), self.data.get("email"))
        self.assertEqual(response.data.get("postId"), self.data.get("postId"))

    def test_post_new_comments_no_auth(self):
        """Unautheticated attempt of comment creation fails."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detailed_after_post_auth(self):
        """Successfully retrive object after calling POST."""
        post_response = self.client.post(self.url_list, self.data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        comment_id = post_response.data["id"]
        detail_url = reverse("comments-detail", kwargs={"pk": comment_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_auth(self):
        """Successfully delete comment authenticated."""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_no_auth(self):
        """Fail to delete comment unauthenticated."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partially_update_comment_auth(self):
        """A comment name patched correctly."""
        data = {"name": "Patch is ready"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), data.get("name"))

    def test_partially_update_comment_no_auth(self):
        """An unauthenticated comment patch fails."""
        self.client.force_authenticate(user=None, token=None)
        data = {"name": "Patch is ready"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_comment_update_auth(self):
        """A comment updated correctly."""
        response = self.client.put(self.url_detail, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.new_data.get("name"))
        self.assertEqual(response.data.get("body"), self.new_data.get("body"))
        self.assertEqual(
            response.data.get("email"),
            self.new_data.get("email"),
        )
        self.assertEqual(
            response.data.get("postId"),
            self.new_data.get("postId"),
        )

    def test_full_comment_update_no_auth(self):
        """An unauthenticated comment update fails."""
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(self.url_detail, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
