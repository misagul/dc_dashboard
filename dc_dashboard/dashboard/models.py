from django.db import models
from datetime import datetime

class Cookie(models.Model):
    cookie_name = models.CharField(max_length=255)
    cookie_text = models.TextField()
    cookie_date = models.CharField(default=datetime.now().strftime("%d.%m.%Y %H:%M:%S"), max_length=255)
    cookie_count = models.IntegerField(default=0)
    cookie_status = models.BooleanField(default=True)

class Channel(models.Model):
    channel_id = models.IntegerField(unique=True)
    channel_limit = models.IntegerField()
    channel_reset = models.IntegerField()
    channel_next_reset = models.CharField(default=datetime.now().strftime("%d.%m.%Y %H:%M:%S"), max_length=255)

class Usage(models.Model):
    usage_user_id = models.IntegerField()
    usage_channel_id = models.IntegerField()
    usage_count = models.IntegerField()


