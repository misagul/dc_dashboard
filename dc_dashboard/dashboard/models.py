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

class Usage(models.Model):
    user_id = models.IntegerField()
    channel_id = models.IntegerField()
    usage = models.IntegerField()

    def __str__(self):
        return f"{self.user_id}"