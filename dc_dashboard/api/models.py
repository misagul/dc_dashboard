from django.db import models

class Bot(models.Model):
    bot_id = models.IntegerField()
    channels = models.ManyToManyField('api.Channel', related_name='bot_channels')
    cookies = models.ManyToManyField('api.Cookie', related_name="bot_cookies")

class Cookie(models.Model):
    name = models.CharField(max_length=255)
    cookie = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return self.name

class Channel(models.Model):
    channel_id = models.IntegerField()
    channel_limit = models.IntegerField()
    channel_reset = models.IntegerField()

class Usage(models.Model):
    user_id = models.IntegerField()
    channel_id = models.IntegerField()
    usage = models.IntegerField()