from django.test import TestCase
from ..models import Post, Comment
from django.conf import settings


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Fixtures for the tests."""
        super().setUpClass()
        cls.long_text = "Lorem ipsum dolor sit amet. " * 3
        cls.post = Post.objects.create(
            title="Test Post",
            body=cls.long_text,
        )

        cls.comment = Comment.objects.create(
            name="Test comment",
            email="comment@test.com",
            body=cls.long_text,
            postId=cls.post,
        )

    def test_models_have_correct_object_names(self):
        """Test object representation from __str__."""
        post_str = str(self.post)
        self.assertEqual(self.long_text[: settings.POST_LENGTH], post_str)

        comment_str = str(self.comment)
        self.assertEqual(self.long_text[: settings.POST_LENGTH], comment_str)

    def test_posts_user_default_value(self):
        """Test user id default in Post model."""
        self.assertTrue(self.post.user == settings.DEFAULT_USER_ID)

    def test_post_model_have_correct_verbose_names(self):
        """Post model has a verbose name."""
        field_verboses = {
            "title": "Title of the post",
            "body": "Body of the post",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name,
                    expected_value,
                )

    def test_comment_model_have_correct_verbose_names(self):
        """Comment model has a verbose name."""
        group_field_verboses = {
            "body": "Body of the comment",
        }
        for field, expected_value in group_field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.comment._meta.get_field(field).verbose_name,
                    expected_value,
                )

    def test_post_model_have_correct_help_text(self):
        """Post model help_text equals to expected."""
        field_help_texts = {
            "title": "Enter post title",
            "body": "Enter post text",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, expected_value
                )

    def test_comment_model_have_correct_help_text(self):
        """Comment model help_text equals to expected."""
        field_help_texts = {
            "body": "Enter comment text",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.comment._meta.get_field(field).help_text,
                    expected_value,
                )
