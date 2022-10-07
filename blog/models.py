from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name='title')
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

