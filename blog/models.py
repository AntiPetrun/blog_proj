from django.db import models


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
    author = models.ForeignKey(
        'auth.user',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def rating(self):
        return self.feedback.aggregate(models.Avg('rating')).get('rating__avg')

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


class Feedback(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='author'
    )
    body = models.TextField()
    date = models.DateField(
        auto_now_add=True
    )
    rating = models.IntegerField(
        default=1
    )
