from django.shortcuts import render
from blog_app.models import Post


def home(request):
    posts = Post.objects.all()
    recent_posts = Post.objects.all().order_by('-created')[:3]
    return render(request, template_name='home_app/index.html', context={'posts': posts, 'recent_posts': recent_posts})
