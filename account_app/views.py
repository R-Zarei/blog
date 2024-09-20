from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, decorators
from .forms import LoginForm, RegisterForm, EditUserForm, EditProfileForm


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

@decorators.login_required
def edit_profile_view(request):
    user = request.user
    # print(user.profile.image.url)
    if request.method == 'POST':
        user_form = EditUserForm(data=request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=user.profile)

    return render(request, 'account_app/edit_profile.html', {'form': user_form, 'form2': profile_form})
