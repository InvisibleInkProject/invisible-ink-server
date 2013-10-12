import django
from django.db import models
from tastypie.models import create_api_key

class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    location_lat = models.FloatField()
    location_lon = models.FloatField()

