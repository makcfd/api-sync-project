from django.db import models

from django.conf import settings


class Post(models.Model):
    """Model for Post object."""

    # TODO make max length
    title = models.TextField(
        verbose_name="Title of the post",
        help_text="Enter post title",
    )
    body = models.TextField(
        verbose_name="Body of the post",
        help_text="Enter post text",
    )
    user = models.IntegerField(
        default=settings.DEFAULT_USER_ID,
        verbose_name="user",
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ("id",)

    def __str__(self):
        return self.body[: settings.POST_LENGTH]


class Comment(models.Model):
    """Model for Comment object."""

    # TODO make max length
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
        return self.body[: settings.POST_LENGTH]
