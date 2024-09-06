from django.shortcuts import render
from .models import Post


def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    recent_posts = Post.objects.all().order_by('-created')[:3]
    return render(request, 'blog_app/post_details.html', {'post': post, 'recent_posts': recent_posts})


def post_list(request):
    posts = Post.objects.all()
    recent_posts = Post.objects.all().order_by('-created')[:3]
    return render(request, template_name='blog_app/posts_list.html',
                  context={'posts': posts, 'recent_posts': recent_posts})

