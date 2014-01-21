from django.conf.urls import url
from django.http import HttpResponse
from django.views.generic import View
from ink.models import Message, User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

import json
import math

class MessageResource(ModelResource):
    distance = fields.FloatField(attribute='distance', blank=True, null=True)

    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        authentication = Authentication()
        authorization = Authorization() #TODO
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>{})/(?P<latitude>([\+-]?\d+\.\d+)),(?P<longitude>([\+-]?\d+\.\d+))/$".format(self._meta.resource_name), self.wrap_view('dispatch_list_with_geo'), name="api_dispatch_list_with_geo"),
        ]

    def dispatch_list_with_geo(self, request, latitude, longitude, **kwargs):
        latitude = float(latitude)
        longitude = float(longitude)

        return self.dispatch_list(request, latitude=latitude, longitude=longitude, **kwargs)

    def apply_sorting(self, obj_list, options=None):
        return sorted(obj_list, key=lambda msg: msg.distance)

    def obj_get_list(self, bundle, **kwargs):
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']
        def distance(message):
            def distance_between(lat1, lon1, lat2, lon2):
                """
                Distance between two coordinates given in angles. Algorithm taken from:
                http://www.movable-type.co.uk/scripts/latlong.html
                """
                R = 6371
                dLat = math.radians(lat2 - lat1)
                dLon = math.radians(lon2 - lon1)
                lat1 = math.radians(lat1)
                lat2 = math.radians(lat2)

                a = math.sin(dLat/2)**2 + math.sin(dLon/2)**2 * math.cos(lat1) * math.cos(lat2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return R * c

            def distance_to(location):
                return distance_between(latitude, longitude, location[0], location[1])

            return distance_to((message.location_lat, message.location_lon))

        messages = super(MessageResource, self).obj_get_list(bundle, **kwargs)
        for message in messages:
            message.distance = distance(message)
        return messages

