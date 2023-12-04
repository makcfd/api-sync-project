from django.db import models

from django.conf import settings


class Post(models.Model):
    """Model for Post object."""

    title = models.TextField(
        verbose_name="Title of the post",
        help_text="Enter post title",
        max_length=200,
    )
    body = models.TextField(
        verbose_name="Body of the post",
        help_text="Enter post text",
    )
    user = models.IntegerField(
        default=settings.DEFAULT_USER_ID,
        verbose_name="user",
    )

    def json(self):
        return {
            "title": self.title,
            "body": self.body,
            "user": self.user,
        }

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ("id",)

    def __str__(self):
        return self.body[: settings.POST_LENGTH]


class Comment(models.Model):
    """Model for Comment object."""

    name = models.TextField(
        max_length=200,
    )
    email = models.EmailField()
    body = models.TextField(
        verbose_name="Body of the comment",
        help_text="Enter comment text",
    )
    postId = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def json(self):
        return {
            "name": self.name,
            "body": self.body,
            "email": self.email,
            "postId": self.postId,
        }

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ("id",)

    def __str__(self):
        return self.body[: settings.POST_LENGTH]
