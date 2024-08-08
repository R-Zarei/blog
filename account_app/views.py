from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    return render(request, template_name='account_app/register.html')


def login_view(request):
    if not request.user.is_authenticated:   # can use .is_anonymous instead .is_authenticated.
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
