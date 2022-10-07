from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from blog.forms import PostForm
from blog.models import Post


def post_list(request: HttpRequest):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)


def post_detail(request: HttpRequest, post_pk: int):
    post = Post.objects.get(pk=post_pk)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


def post_create(request: HttpRequest):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_create.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.published_date = datetime.now()
            post.save()
            return post_detail(request, post_pk=post.pk)


def post_update(request: HttpRequest, post_pk: int):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/post_update.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.published_date = datetime.now()
            post.save()
            return post_detail(request, post_pk=post.pk)


def post_delete(request: HttpRequest, post_pk: int):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/post_delete.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.delete()
            return post_list(request)
