from django.http import HttpResponse
from .models import Cookie, Bot, Channel, Usage
from django.shortcuts import render

def index(request):
    return HttpResponse("Deneme")

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