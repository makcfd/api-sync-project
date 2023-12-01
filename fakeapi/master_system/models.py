from django.contrib.auth import get_user_model
from django.db import models

from django.conf import settings

# create user with specific id and link it to the Post and Comments
# User = get_user_model()

POST_LENGTH = 10


class Post(models.Model):
    """Model fro Post object"""

    title = models.TextField(
        verbose_name="Title of the post",
        help_text="Enter post title",
    )
    body = models.TextField(
        verbose_name="Body of the post",
        help_text="Enter post text",
    )
    # TODO move defaul value to config or settings
    user = models.IntegerField(
        default=settings.DEFAULT_USER_ID,
        verbose_name="user",
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ("id",)

    def __str__(self):
        return self.body[:POST_LENGTH]


class Comment(models.Model):
    """Model for Comment object"""

    name = models.TextField()
    email = models.EmailField()
    body = models.TextField(
        verbose_name="Body of the comment",
        help_text="Enter comment text",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ("id",)

    def __str__(self):
        return self.body[:POST_LENGTH]
