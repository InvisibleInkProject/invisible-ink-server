import django
from django.db import models
from tastypie.models import create_api_key

class User(django.contrib.auth.models.User):
    birthday = models.DateField()
    gender = models.CharField(max_length=1)
    nationality = models.CharField(max_length=40, null=True, blank=True)

class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User)
    text = models.TextField()
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    radius = models.FloatField()

    def __unicode__(self):
        return "{}, {} ({}): {}".format(self.location_lat, self.location_lon, self.radius, self.text)

models.signals.post_save.connect(create_api_key, sender=User)
