from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog_app/post_details.html', {'post': post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, template_name='blog_app/posts_list.html', context={'posts': posts})


def category_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.post_set.all()
    return render(request, 'blog_app/category_details.html', {'posts': posts, 'category': category})
