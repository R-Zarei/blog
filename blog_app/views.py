from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, Message, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MessageForm
from django.views.generic import DetailView, ListView, FormView, CreateView
from django.urls import reverse, reverse_lazy
from .mixins import CustomLoginRequiredMixin  # custom mixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:   # if user is logged in send user liked status else send False.
        is_liked = request.user.likes.filter(post_id=post.id).exists()
    else:
        is_liked = False
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        comment = Comment.objects.create(post=post, user=request.user, body=body, parent_id=parent_id)
        # object_dict = model_to_dict(comment)
        if comment.user.profile.image:
            user_image = comment.user.profile.image.url
        else:
            user_image = None
        data = {
            'id': comment.id,
            'date': comment.created,
            'user_name': comment.user.username,
            'user_img_url': user_image,
            'body': body,
        }
        return JsonResponse(data)

    return render(request, 'blog_app/post_details.html', {'post': post, 'is_liked': is_liked})


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


@login_required
def like_post(request, slug, pk):
    try:
        like = Like.objects.get(post__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({'status': 'unliked', 'like_num': Post.objects.get(slug=slug).likes.count()})
    except:
        Like.objects.create(post_id=pk, user_id=request.user.id)
        return JsonResponse({'status': 'liked', 'like_num': Post.objects.get(slug=slug).likes.count()})


# ---- Class base views ----
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_details.html'  # default is model(post)_detail .
    # context_object_name = 'post'   # default is model_name(post).
    # slug_field = 'post_slug_field'   # default is "slug". is for slug filed name in model.
    # slug_url_kwarg = 'slug_item'   # default is "slug". in url.
    # pk_url_kwarg = 'pk'
    queryset = Post.objects.filter(published=True)  # send filtered objects.

    def get_context_data(self, **kwargs):  # send context for template.
        context = super().get_context_data(**kwargs)
        context['name'] = "reza"
        return context


class PostListView(CustomLoginRequiredMixin,
                   ListView):  # use CustomLoginRequiredMixin for redirect users that not logged to login page.
    model = Post
    template_name = 'blog_app/posts_list.html'  # default is model name_list (post_list).
    context_object_name = 'posts'
    paginate_by = 2  # most use "page_obj" in template for pagination.


class ContactUsView(FormView):
    template_name = 'blog_app/contact_us.html'
    form_class = MessageForm
    success_url = reverse_lazy('home_app:home')  # if we use reverse, we get error.

    def form_valid(self, form):
        form_data = form.cleaned_data
        Message.objects.create(**form_data)  # or create(title=form_data['title'], body= ...).
        return super().form_valid(form)


class ContactUsView2(CreateView):
    # CreateView default create form for model we can use a created form with "form_class = ".
    # form_class = MessageForm
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('home_app:home')
    template_name = 'blog_app/contact_us.html'  # default is (form name)_form : "message_form".

    def get_context_data(self, **kwargs):  # for send context.
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.all()
        return context

    def form_valid(self, form):  # if form is valid email = custom email.
        instance = form.save(commit=False)
        instance.email = self.request.user.email
        instance.save()
        return super().form_valid(form)
