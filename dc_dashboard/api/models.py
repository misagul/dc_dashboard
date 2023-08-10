from django.db import models

class Bot(models.Model):
    bot_id = models.IntegerField()
    channels = models.ManyToManyField('api.Channel', related_name='bot_channels')
    cookies = models.ManyToManyField('api.Cookie', related_name="bot_cookies")

class Cookie(models.Model):
    cookie = models.TextField()
    status = models.BooleanField()

class Channel(models.Model):
    channel_id = models.IntegerField()
    channel_limit = models.IntegerField()
    channel_reset = models.IntegerField()

class Usage(models.Model):
    user_id = models.IntegerField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    usage = models.IntegerField()