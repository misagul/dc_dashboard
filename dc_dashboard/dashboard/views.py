from django.http import HttpResponse
from .models import Cookie, Channel, Member
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request, "home.html")

def members(request):
    context = {
        'members': Member.objects.all().order_by('member_user_id')
    }
    return render(request, "members.html", context)

def cookies(request):
    context = {
        'cookies' : Cookie.objects.all()
    }
    return render(request, "cookies.html", context)

def channels(request):
    context = {
        'channels' : Channel.objects.all()
    }
    return render(request, "channels.html", context)

def login_request(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard:home")
            else:
                context = {
                    'error_message': 'User not found.'
                }

    return render(request, "login.html", context=context)

def logout_request(request):
        logout(request)
        return redirect("dashboard:login")