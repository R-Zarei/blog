from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment, Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MessageForm
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse, reverse_lazy


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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_details.html'   # default is model(post)_detail .
    # context_object_name = 'post'   # default is model_name(post).
    # slug_field = 'post_slug_field'   # default is "slug". is for slug filed name in model.
    # slug_url_kwarg = 'slug_item'   # default is "slug". in url.
    # pk_url_kwarg = 'pk'
    queryset = Post.objects.filter(published=True)   # send filtered objects.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = "reza"
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/posts_list.html'   # default is model name_list (post_list).
    context_object_name = 'posts'
    paginate_by = 2   # most use "page_obj" in template for pagination.


class ContactUsView(FormView):
    template_name = 'blog_app/contact_us.html'
    form_class = MessageForm
    success_url = reverse_lazy('home_app:home')   # if we use reverse, we get error.

    def form_valid(self, form):
        form_data = form.cleaned_data
        Message.objects.create(**form_data)   # or create(title=form_data['title'], body= ...).
        return super().form_valid(form)
