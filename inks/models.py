import django
from django.db import models
from tastypie.models import create_api_key

from django.contrib.auth.models import User as DjangoUser

from provider.oauth2.models import Client

#TODO: Move this out of the models file and into a separate file or so
def create_oauth_client_for_user(sender, instance, created, **kwargs):
    if kwargs.get('created') is False:
        return False
    
    client = Client(
            user=DjangoUser.objects.get(id=instance.id), 
            name="Invisible Ink: %s" % instance.username, 
            client_type=1, 
            url="http://server.invisibleink.no"
    )
    client.save()

class User(DjangoUser):
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
models.signals.post_save.connect(create_oauth_client_for_user, sender=User)
