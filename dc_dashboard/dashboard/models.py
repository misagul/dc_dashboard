from django.db import models

class Cookie(models.Model):
    name = models.CharField(max_length=255)
    cookie = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    status = models.BooleanField()

    def __str__(self):
        return f"{self.name}"

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