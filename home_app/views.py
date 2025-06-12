from django.shortcuts import render
from blog_app.models import Post


def home(request):
    posts = Post.objects.all()
    return render(request, template_name='home_app/index.html', context={'posts': posts})


def about(request):
    return render(request, "home_app/about_us.html", {})
