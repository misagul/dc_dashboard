from django.http import HttpResponse
from .models import Cookie, Bot, Channel
from django.shortcuts import render

def index(request):
    return HttpResponse("Deneme")

def members(request):
    context = {
        
    }
    return render(request, "members.html", context)

def cookies(request):
    context = {
        'cookies' : Cookie.objects.all()
    }
    return render(request, "cookies.html", context)