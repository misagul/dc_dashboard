from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from dashboard.models import Cookie, Channel, Usage
from django.core import serializers

def delete_channel(request):
    if request.method == 'POST':
        id = request.POST['data_ch_pk']
        print(id)
        channel = Channel.objects.get(id=id)
        if channel:
            channel.delete()
        return HttpResponse(200)

def add_channel(request):
    if request.method == 'POST':
        channel_id = request.POST['channel_id']
        channel_limit = request.POST['channel_limit']
        channel_reset = request.POST['channel_reset']
        new_channel = Channel(channel_id=channel_id, channel_limit=channel_limit, channel_reset=channel_reset)
        new_channel.save()
        return HttpResponse(new_channel.channel_id)

def get_channels(request):
    data = serializers.serialize("json", Channel.objects.all())
    return HttpResponse(data, content_type="application/json")


