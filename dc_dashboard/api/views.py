from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from dashboard.models import Cookie, Channel, Usage
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import threading
from datetime import datetime, timedelta

def reset_usages():
    channels = Channel.objects.all()
    for channel in channels:
        channel_id = channel.channel_id
        channel_limit = channel.channel_limit
        channel_reset = channel.channel_reset
        channel_next_reset = channel.channel_next_reset

        reset_date = datetime.strptime(channel_next_reset, "%d.%m.%Y %H:%M:%S")
        now = datetime.now()

        if now > reset_date:
            channel.channel_next_reset = (reset_date + timedelta(minutes=channel_reset)).strftime("%d.%m.%Y %H:%M:%S")
            print(channel.channel_next_reset)
            channel.save()
    threading.Timer(100, reset_usages).start()

reset_usages()

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
    cookies = serializers.serialize("json", Cookie.objects.all())
    return HttpResponse(cookies, content_type="application/json")

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
        return HttpResponse(cookie.cookie_name)

def get_usages(request):
    usages = serializers.serialize("json", Usage.objects.all().order_by('usage_user_id'))
    return HttpResponse(usages, content_type="application/json")

@csrf_exempt
def add_usage(request):

    # 0: usage object exist, usage_count 0
    # 1: usage object exist, usage count not 0
    # 2: usage object not exist, new user object created
    # 3: usage object not exist, channel not exist

    if request.method == 'POST':
        usage_user_id = request.POST['usage_user_id']
        usage_channel_id = request.POST['usage_channel_id']
        try:
            usage = Usage.objects.get(usage_user_id=usage_user_id, usage_channel_id=usage_channel_id)
        except:
            usage = None
        
        if usage:
            if usage.usage_count != 0:
                usage.usage_count -= 1
                usage.save()
                
                return HttpResponse("0, usage object exist, usage count not 1")
            return HttpResponse("1, usage object exist, usage_count 0")

        else:
            try:
                channel = Channel.objects.get(channel_id=usage_channel_id)
            except:
                return HttpResponse("3, usage object not exist, channel not exist")
            
            new_usage = Usage(usage_user_id=usage_user_id, usage_channel_id=usage_channel_id, usage_count=channel.channel_limit)
            new_usage.save()
            return HttpResponse("2, usage object not exist, new user object created")

        
