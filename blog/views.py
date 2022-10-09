from datetime import datetime

from django.db.models import Avg
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment, Category, Feedback


def ratings(post_pk: int):
    feedbacks = Feedback.objects.filter(post=post_pk)
    rating = sum([feedback.rating for feedback in feedbacks]) / feedbacks.count()
    return round(rating, 1)


def post_list(request: HttpRequest):
    posts = Post.objects.all().filter(is_published=True).order_by('-created_date')
    categories = Category.objects.all().order_by('name')
    count = posts.count()
    context = {'posts': posts, 'categories': categories, 'count': count}
    return render(request, 'blog/post_list.html', context)


def draft_post_list(request: HttpRequest):
    posts = Post.objects.all().filter(is_published=False).order_by('-created_date')
    categories = Category.objects.all().order_by('name')
    count = posts.count()
    context = {'posts': posts, 'categories': categories, 'count': count}
    return render(request, 'blog/post_list.html', context)


def set_published(request: HttpRequest, post_pk: int):
    post = get_object_or_404(Post, pk=post_pk)
    if post.is_published is False:
        post.is_published = True
        post.save()
        return render(request, 'blog/post_detail.html', {'post': post})
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


def post_detail(request: HttpRequest, post_pk: int):
    post = Post.objects.get(pk=post_pk)
    comments = Comment.objects.filter(post=post_pk)
    count = comments.count()
    rating = ratings(post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.published_date = datetime.now()
            comment.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = CommentForm()
    context = {'post': post, 'comments': comments, 'count': count, 'form': form, 'rating': rating}
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
            return redirect('post_detail', post_pk=post.pk)


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
    categories = Category.objects.all().order_by('name')
    posts = Post.objects.filter(category=category_pk).order_by('-is_published')
    count = posts.count()
    context = {'categories': categories, 'posts': posts, 'count': count}
    return render(request, 'blog/post_list.html', context)


def comment_delete(request: HttpRequest, comment_pk: int, post_pk: int):
    post = Post.objects.get(pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk).delete()
    return redirect('post_detail', post_pk=post.pk)


def feedback_by_post(request: HttpRequest, post_pk: int):
    post = Post.objects.get(pk=post_pk)
    categories = Category.objects.all().order_by('-name')
    feedbacks = Feedback.objects.filter(post=post_pk)
    rating = ratings(post_pk)
    context = {'post': post, 'feedbacks': feedbacks, 'categories': categories, 'rating': rating}
    return render(request, 'blog/feedback_by_post.html', context)


def recommendation_list(request: HttpRequest):
    posts = Post.objects.values('title', 'pk').annotate(Avg('feedback__rating')).order_by('-feedback__rating__avg')
    categories = Category.objects.all().order_by('name')
    count = posts.count()
    context = {'posts': posts, 'categories': categories, 'count': count}
    return render(request, 'blog/post_list.html', context)
