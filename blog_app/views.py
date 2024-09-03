from django.shortcuts import render
from .models import Post


def post_details(request, pk):
    context = Post.objects.get(pk=pk)
    return render(request, 'blog_app/post_details.html', {'post': context})
