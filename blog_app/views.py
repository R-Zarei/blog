from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MessageForm


def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(post=post, user=request.user, body=body, parent_id=parent_id)

    return render(request, 'blog_app/post_details.html', {'post': post})


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    try:
        objects_list = paginator.get_page(page_number)
    except PageNotAnInteger:
        objects_list = paginator.get_page(1)
    except EmptyPage:
        objects_list = paginator.get_page(paginator.num_pages)

    return render(request, template_name='blog_app/posts_list.html', context={'posts': objects_list})


def category_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.post_set.all()
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 2)
    objects_list = paginator.get_page(page_number)

    return render(request, 'blog_app/category_details.html', {'posts': objects_list, 'category': category})


def search_posts(request):
    posts = Post.objects.filter(title__icontains=request.GET.get('q'))
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 1)
    objects_list = paginator.get_page(page_number)

    return render(request, 'blog_app/posts_list.html', {'posts': objects_list})


def contact_us(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MessageForm()

    return render(request, 'blog_app/contact_us.html', {'form': form})
