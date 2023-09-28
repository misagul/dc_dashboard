from django.http import HttpResponse, JsonResponse
from dashboard.models import Cookie, Channel, Usage
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import threading
from datetime import datetime, timedelta

def reset_usages():
    channels = Channel.objects.all()
    for channel in channels:

        reset_date = datetime.strptime(channel.channel_next_reset, "%d.%m.%Y %H:%M:%S")
        now = datetime.now()

        if now > reset_date:
            channel.channel_next_reset = (datetime.now() + timedelta(hours=channel.channel_reset)).strftime("%d.%m.%Y %H:%M:%S")
            channel.save()
            
            Usage.objects.filter(usage_channel_id=channel.channel_id).update(usage_left=channel.channel_limit)                
            
    threading.Timer(60, reset_usages).start()

# reset_usages()

def get_usages(request):
    usages = serializers.serialize("json", Usage.objects.all().order_by('usage_user_id'))
    return HttpResponse(usages, content_type="application/json")

@csrf_exempt
def get_usage(request):
    if request.method == 'POST':
        usage_user_id = request.POST['usage_user_id']
        usage_channel_id = request.POST['usage_channel_id']
        try:
            usage = Usage.objects.get(usage_user_id=usage_user_id, usage_channel_id=usage_channel_id)
        except:
            usage = None
        
        if usage:
            return HttpResponse(usage.usage_left)
        
        return HttpResponse(-1)
            
@csrf_exempt
def add_usage(request):

    # 0: usage object exist, usage_left 0
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
            if usage.usage_left != 0:
                usage.usage_left -= 1
                usage.save()
                
                return HttpResponse("0, usage object exist, usage count not 1")
            return HttpResponse("1, usage object exist, usage_left 0")

        else:
            try:
                channel = Channel.objects.get(channel_id=usage_channel_id)
            except:
                return HttpResponse("3, usage object not exist, channel not exist")
            
            new_usage = Usage(usage_user_id=usage_user_id, usage_channel_id=usage_channel_id, usage_left=channel.channel_limit)
            new_usage.save()
            return HttpResponse("2, usage object not exist, new user object created")


def get_channels(request):
    data = serializers.serialize("json", Channel.objects.all())
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def get_channel_limit(request):
    channel_id = request.POST['channel_id']
    try:
        channel = Channel.objects.get(channel_id=channel_id)
    except:
        channel = None
    
    if channel:
        return HttpResponse(channel.channel_limit)
    
    return HttpResponse(-1)

def add_channel(request):
    if request.method == 'POST':
        channel_id = request.POST['channel_id']
        channel_limit = request.POST['channel_limit']
        channel_reset = request.POST['channel_reset']
        channel_next_reset =  (datetime.now() + timedelta(hours=channel_reset)).strftime("%d.%m.%Y %H:%M:%S")
        new_channel = Channel(channel_id=channel_id, channel_limit=channel_limit, channel_reset=channel_reset, channel_next_reset=channel_next_reset)
        new_channel.save()
        return HttpResponse(new_channel)

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

@csrf_exempt
def get_current_cookie(request):
    current_cookie = Cookie.objects.get(cookie_is_current=True)
    if current_cookie.cookie_count > current_cookie.cookie_limit:
        next_cookie = Cookie.objects.filter(pk__gt = current_cookie.pk).order_by('pk').first()
        if next_cookie == None:
            next_cookie = Cookie.objects.all().order_by('pk').first()
        current_cookie.cookie_is_current = False
        current_cookie.cookie_count = 0
        next_cookie.cookie_is_current = True
        current_cookie.save()
        next_cookie.save()
        return HttpResponse(next_cookie)
    print(current_cookie.pk)
    return HttpResponse(current_cookie)
    

@csrf_exempt
def get_cookies(request):
    cookies = serializers.serialize("json", Cookie.objects.all())
    return HttpResponse(cookies, content_type="application/json")

def add_cookie(request):
    if request.method == 'POST':
        cookie_name = request.POST['cookie_name']
        cookie_text = request.POST['cookie_text']
        cookie_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        new_cookie = Cookie(cookie_name=cookie_name, cookie_text=cookie_text, cookie_date=cookie_date)
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


