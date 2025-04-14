from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('posts/<slug:slug>/', views.post_details, name='post_details'),
    path('posts/', views.post_list, name='posts'),
    path('category/<int:pk>/', views.category_details, name='category_details'),
    path('search/', views.search_posts, name='search_posts'),
    path('contactus/', views.contact_us, name='contact_us'),
    path('like/<slug:slug>/<int:pk>/', views.like_post, name='like_post'),
]
