from django.contrib import admin
from django.urls import path, include

from blog.views import post_list, post_detail, post_create, post_update, post_delete

urlpatterns = [
    path('posts', post_list, name='post_list'),
    path('post/detail/<int:post_pk>', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('post/update/<int:post_pk>', post_update, name='post_update'),
    path('post/delete/<int:post_pk>', post_delete, name='post_delete'),
]
