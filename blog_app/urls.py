from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('posts/<int:pk>/', views.post_details, name='post_details'),
    path('posts', views.post_list, name='posts'),
]
