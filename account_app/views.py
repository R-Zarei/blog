from django.shortcuts import render


def login(request):
    return render(request, template_name='account_app/login.html', context={})
