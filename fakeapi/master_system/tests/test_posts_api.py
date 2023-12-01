from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()


class PostsAPITests(APITestCase):
    url_list = reverse("posts-list")
    url_detail = reverse("posts-detail", kwargs={"pk": 101})

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
        self.data = {
            "title": "Amazing post",
            "body": "Something about post",
        }

    def test_get_list_no_auth(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url_list)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            # TODO what is response data here
            # response.data,
        )

    def test_get_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_post_new_post_auth(self):
        response = self.client.post(
            self.url_list,
            self.data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detailed_auth(self):
        # First, create a new post
        post_response = self.client.post(
            self.url_list,
            self.data,
            format="json",
        )
        # Ensure the post was created successfully
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the newly created post
        post_id = post_response.data["id"]
        detail_url = reverse("posts-detail", kwargs={"pk": post_id})

        # Now, try to retrieve the newly created post
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO checking response data
    # https://www.django-rest-framework.org/api-guide/testing/#checking-the-response-data
    # self.assertEqual(response.data["body"], "Something about post")
    # self.assertEqual(response.data["user"], settings.DEFAULT_USER_ID)

    # def test_userprofile_with_update_without_passing_query_params(self):
    #     data_update = {"name": "test", "email": "test@12.com", "bio": "hello"}
    #     resp = self.client.patch(f"{self.user_profile}?", data_update)
    #     self.assertEqual(resp.status_code, 400)

    # def test_get_detail_no_auth(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(
    #         response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
    #     )

    # def test_get_detail(self):
    #     response = self.client.get(self.url_detail, **self.bearer_token)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    # def test_delete_customer_authenticated(self):
    #     response = self.client.delete(self.url_detail)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,)
