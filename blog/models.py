from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import related


class Post(models.Model):
    title = models.CharField(
        max_length=64,
        verbose_name='title'
    )
    body = models.TextField()
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    published_date = models.DateTimeField(
        auto_now_add=True
    )
    is_published = models.BooleanField(
        default=False
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    published_date = models.DateTimeField(
        auto_now_add=True
    )
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='author'
    )

    def __str__(self):
        return self.body


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='title'
    )

    def __str__(self):
        return self.name
