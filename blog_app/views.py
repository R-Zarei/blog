from django.shortcuts import render
from .models import Post


def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog_app/post_details.html', {'post': post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, template_name='blog_app/posts_list.html', context={'posts': posts})
