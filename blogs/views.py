from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import BlogPostForm


def index(request):
    return render(request, 'blogs/index.html')


def posts(request):
    """Выводит список постов"""
    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)


def post(request, blogpost_id):
    """Выводит одну статью и все её записи."""
    post = BlogPost.objects.get(id=blogpost_id)
    text = post.text
    context = {'post': post, 'text': text}
    return render(request, 'blogs/post.html', context)


@login_required
def new_post(request):
    """Добавляет новую статью"""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = BlogPostForm()
    else:
        # Отправлены данные POST; обработать данные
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:posts')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, blogpost_id):
    """Редактирует существующую запись"""
    post = BlogPost.objects.get(id=blogpost_id)

    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', blogpost_id=blogpost_id)

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)