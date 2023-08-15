from django.shortcuts import render
from dashboard.models import Cookie, Channel, Usage

def delete_channel(request, channel_id):
    print("delete channel request")
    Channel.objects.get(channel_id=channel_id).delete()
    context = {
        'channels' : Channel.objects.all()
    }
    return render(request, "channels.html", context)