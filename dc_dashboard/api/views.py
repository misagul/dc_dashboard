from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from dashboard.models import Cookie, Channel, Usage
from django.core import serializers
import json

def get_channels(request):
    data = serializers.serialize("json", Channel.objects.all())
    return HttpResponse(data, content_type="application/json")

def add_channel(request):
    if request.method == 'POST':
        channel_id = request.POST['channel_id']
        channel_limit = request.POST['channel_limit']
        channel_reset = request.POST['channel_reset']
        new_channel = Channel(channel_id=channel_id, channel_limit=channel_limit, channel_reset=channel_reset)
        new_channel.save()
        return HttpResponse(new_channel.channel_id)
    
def update_channel(request):
    if request.method == 'POST':
        channel_pk = request.POST['channel_pk']
        channel_id = request.POST['channel_id']
        channel_limit = request.POST['channel_limit']
        channel_reset = request.POST['channel_reset']

        channel = Channel.objects.get(pk=channel_pk)
        channel.channel_id = channel_id
        channel.channel_limit = channel_limit
        channel.channel_reset = channel_reset
        channel.save()
        
        data = serializers.serialize("json", [channel])
        return HttpResponse(data, content_type="application/json")

def delete_channel(request):
    if request.method == 'POST':
        id = request.POST['data_ch_pk']
        print(id)
        channel = Channel.objects.get(id=id)
        if channel:
            channel.delete()
        return HttpResponse(channel.channel_id)




def get_cookies(request):
    data = serializers.serialize("json", Cookie.objects.all())
    return HttpResponse(data, content_type="application/json")

def add_cookie(request):
    if request.method == 'POST':
        cookie_name = request.POST['cookie_name']
        cookie_text = request.POST['cookie_text']
        print(cookie_name, cookie_text)
        new_cookie = Cookie(cookie_name=cookie_name, cookie_text=cookie_text)
        new_cookie.save()
        return HttpResponse(new_cookie.cookie_name)
    
def update_cookie(request):
    if request.method == 'POST':
        cookie_pk = request.POST['cookie_pk']
        cookie_name = request.POST['cookie_name']
        cookie_text = request.POST['cookie_text']

        cookie = Cookie.objects.get(pk=cookie_pk)
        cookie.cookie_name = cookie_name
        cookie.cookie_text = cookie_text
        cookie.save()
        
        data = serializers.serialize("json", [cookie])
        return HttpResponse(data, content_type="application/json")

def delete_cookie(request):
    if request.method == 'POST':
        id = request.POST['cookie_pk']
        print(id)
        cookie = Cookie.objects.get(id=id)
        if cookie:
            cookie.delete()
        return HttpResponse(200)

