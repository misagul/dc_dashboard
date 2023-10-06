from django.http import HttpResponse, JsonResponse
from dashboard.models import Cookie, Channel, Member
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import threading
import time
from datetime import datetime, timedelta

def reset_usages():
    channels = Channel.objects.all()
    for channel in channels:
        reset_date = datetime.strptime(channel.channel_next_reset, "%d.%m.%Y %H:%M:%S")
        now = datetime.now()
        print(now, reset_date)
        if now > reset_date:
            print(channel.channel_id)
            channel.channel_next_reset = (datetime.now() + timedelta(hours=channel.channel_reset)).strftime("%d.%m.%Y %H:%M:%S")
            channel.save()
            
            Member.objects.filter(member_channel_id=channel.channel_id).update(member_usage_left=channel.channel_limit)                
    threading.Timer(3600, reset_usages).start()
    
# reset_usages()

def get_members(request):
    members = serializers.serialize("json", Member.objects.all().order_by('member_user_id'))
    return HttpResponse(members, content_type="application/json")

@csrf_exempt
def get_member_usage(request):
    if request.method == 'POST':
        member_user_id = request.POST['member_user_id']
        member_channel_id = request.POST['member_channel_id']
        try:
            member = Member.objects.get(member_user_id=member_user_id, member_channel_id=member_channel_id)
            return HttpResponse(member.member_usage_left)
        except:
            channel = Channel.objects.get(channel_id=member_channel_id)
            new_member = Member(member_user_id=member_user_id, member_channel_id=member_channel_id, member_usage_left=channel.channel_limit)
            new_member.save()
            return HttpResponse(new_member.member_usage_left)
            
@csrf_exempt
def add_member_usage(request):

    # 0: member object exist, usage_ 0
    # 1: member object exist, member count not 0
    # 2: member object not exist, new user object created
    # 3: member object not exist, channel not exist

    if request.method == 'POST':
        member_user_id = request.POST['member_user_id']
        member_channel_id = request.POST['member_channel_id']
        try:
            member = Member.objects.get(member_user_id=member_user_id, member_channel_id=member_channel_id)
        except:
            member = None
        
        if member:
            if member.member_usage_left != 0:
                member.member_usage_left -= 1
                member.save()
                
                return HttpResponse("0, member object exist, member count not 1")
            return HttpResponse("1, member object exist, usage_left 0")

        else:
            try:
                channel = Channel.objects.get(channel_id=member_channel_id)
            except:
                return HttpResponse("3, member object not exist, channel not exist")
            
            new_member = Member(member_user_id=member_user_id, member_channel_id=member_channel_id, member_usage_left=channel.channel_limit-1)
            new_member.save()
            return HttpResponse("2, member object not exist, new user object created")

@csrf_exempt
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
        channel_next_reset =  (datetime.now() + timedelta(hours=int(channel_reset))).strftime("%d.%m.%Y %H:%M:%S")
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
    try:
        current_cookie = Cookie.objects.get(cookie_is_current=True)
    except:
        current_cookie = Cookie.objects.filter(cookie_status=True).order_by('pk').first()
    if current_cookie.cookie_count > current_cookie.cookie_limit:
        next_cookie = Cookie.objects.filter(pk__gt = current_cookie.pk, cookie_status=True).order_by('pk').first()
        if next_cookie == None:
            next_cookie = Cookie.objects.filter(cookie_status=True).order_by('pk').first()
            if next_cookie == None:
                return HttpResponse(-1)

        current_cookie.cookie_is_current = False
        current_cookie.cookie_count = 0
        next_cookie.cookie_is_current = True
        current_cookie.save()
        next_cookie.save()
        data = serializers.serialize("json", [next_cookie])
        return HttpResponse(data, content_type="application/json")

    data = serializers.serialize("json", [current_cookie])
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def update_cookie_status(request):
    if request.method == 'POST':
        cookie_pk = request.POST['cookie_pk']
        cookie_status = request.POST['cookie_status']
        cookie = Cookie.objects.get(pk=cookie_pk)
        cookie.cookie_status = cookie_status
        cookie.save()

@csrf_exempt
def add_cookie_usage(request):
    if request.method == 'POST':
        cookie_pk = request.POST['cookie_pk']
        cookie = Cookie.objects.get(pk=cookie_pk)
        cookie.cookie_count += 1
        cookie.save()
        return HttpResponse(1)

@csrf_exempt
def get_cookies(request):
    cookies = serializers.serialize("json", Cookie.objects.all())
    return HttpResponse(cookies, content_type="application/json")

def add_cookie(request):
    if request.method == 'POST':
        cookie_name = request.POST['cookie_name']
        cookie_text = request.POST['cookie_text']
        cookie_limit = request.POST['cookie_limit']
        cookie_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        new_cookie = Cookie(cookie_name=cookie_name, cookie_text=cookie_text, cookie_date=cookie_date, cookie_limit=cookie_limit)
        new_cookie.save()
        return HttpResponse(new_cookie.cookie_name)

def update_cookie(request):
    if request.method == 'POST':
        cookie_pk = request.POST['cookie_pk']
        cookie_name = request.POST['cookie_name']
        cookie_limit = request.POST['cookie_limit']

        cookie = Cookie.objects.get(pk=cookie_pk)
        cookie.cookie_name = cookie_name
        cookie.cookie_limit = cookie_limit
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


