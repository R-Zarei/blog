from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, template_name='account_app/register.html', context={'form': form})


def login_view(request):
    if request.user.is_authenticated:  # can use not .is_anonymous instead .is_authenticated.
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get('username'))
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, template_name='account_app/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
