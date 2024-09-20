from django.urls import path
from . import views


app_name = 'account_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register_view, name='signup'),
    path('profile/', views.edit_profile_view, name='profile'),
]
