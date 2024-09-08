from blog_app.models import Post, Category


def recent_posts(request):
    return {'recent_posts': Post.objects.order_by('-created')[:3]}


def categorise(request):
    return {'categorise': Category.objects.all()}
