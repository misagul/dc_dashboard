from django.http import HttpResponse
from .models import Cookie, Bot, Channel, Usage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def index(request):
    return render(request, "index.html")

def usages(request):
    context = {
        'usages': Usage.objects.all().order_by('user_id')
    }
    return render(request, "usages.html", context)

def cookies(request):
    context = {
        'cookies' : Cookie.objects.all()
    }
    return render(request, "cookies.html", context)

def login_request(request):
    if request.user:
        return redirect("cookies")

    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("cookies")
            else:
                context = {
                    'error_message': 'User not found.'
                }

    return render(request, "login.html", context=context)