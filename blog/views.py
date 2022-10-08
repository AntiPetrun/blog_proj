from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from blog.forms import PostForm
from blog.models import Post, Comment, Category


def post_list(request: HttpRequest):
    posts = Post.objects.all().filter(is_published=True).order_by('-created_date')
    categories = Category.objects.all().order_by('-name')
    context = {'posts': posts, 'categories': categories}
    return render(request, 'blog/post_list.html', context)


def draft_post_list(request: HttpRequest):
    posts = Post.objects.all().filter(is_published=False).order_by('-created_date')
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)


def set_published(request: HttpRequest, post_pk: int):
    post = get_object_or_404(Post, pk=post_pk)
    if post.is_published is False:
        post.is_published = True
        post.save()
        return render(request, 'blog/post_detail.html', {'post': post})
    return render(request, 'blog/post_detail.html', {'post': post})


def post_detail(request: HttpRequest, post_pk: int):
    post = Post.objects.get(pk=post_pk)
    comments = Comment.objects.filter(post=post_pk)
    count = comments.count()
    context = {'post': post, 'comments': comments, 'count': count}
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


def by_category(request: HttpRequest, category_pk: int):
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category_pk).order_by('-is_published')
    count = posts.count()
    context = {'categories': categories, 'posts': posts, 'count': count}
    return render(request, 'blog/post_list.html', context)
