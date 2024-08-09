from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    context = {'errors': []}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        temp = True
        if User.objects.filter(username=username).exists():
            context['errors'].append('User already exists')
            temp = False
        if password != password2:
            context['errors'].append('Passwords do not match')
        elif temp:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/')

    return render(request, template_name='account_app/register.html', context=context)


def login_view(request):
    if not request.user.is_authenticated:  # can use .is_anonymous instead .is_authenticated.
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

        return render(request, template_name='account_app/login.html', context={})

    else:
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')
