from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from dashboard.models import Cookie, Channel, Usage

def delete_channel(request):
    if request.method == 'POST':
        id = request.POST['id']
        channel = Channel.objects.get(id=id)
        if channel:
            channel.delete()
        return HttpResponse(200)

def add_channel(request):
    if request.method == 'POST':
        channel_id = request.POST['channel_id']
        channel_limit = request.POST['channel_limit']
        channel_reset = request.POST['channel_reset']
        new_channel = Channel(channel_id=channel_id, channel_limit=channel_limit, channel_reset=channel_reset).save()
        
        return HttpResponse(f"{new_channel}")
    
