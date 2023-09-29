from django.db import models
from datetime import datetime

class Cookie(models.Model):
    cookie_name = models.CharField(max_length=255)
    cookie_text = models.TextField()
    cookie_date = models.CharField(max_length=255)
    cookie_count = models.IntegerField(default=0)
    cookie_limit = models.IntegerField(default=20)
    cookie_status = models.BooleanField(default=True)
    cookie_is_current = models.BooleanField()

class Channel(models.Model):
    channel_id = models.IntegerField(unique=True)
    channel_limit = models.IntegerField()
    channel_reset = models.IntegerField()
    channel_next_reset = models.CharField(max_length=255)

class Member(models.Model):
    member_user_id = models.IntegerField()
    member_channel_id = models.IntegerField()
    member_usage_left = models.IntegerField()


