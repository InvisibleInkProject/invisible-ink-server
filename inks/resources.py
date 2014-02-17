from django.conf.urls import url
from django.http import HttpResponse
from django.views.generic import View
from inks.models import Message, User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

import json
import logging
import math

class MessageResource(ModelResource):
    distance = fields.FloatField(attribute='distance', blank=True, null=True)

    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>{})/(?P<latitude>([\+-]?\d+\.\d+)),(?P<longitude>([\+-]?\d+\.\d+)),(?P<windowRadius>([\+-]?\d+\.\d+))/$".format(self._meta.resource_name), self.wrap_view('dispatch_list_with_geo'), name="api_dispatch_list_with_geo"),
        ]

    def dispatch_list_with_geo(self, request, latitude, longitude, windowRadius, **kwargs):
        latitude = float(latitude)
        longitude = float(longitude)
        windowRadius = float(windowRadius)

        return self.dispatch_list(request, latitude=latitude, longitude=longitude, windowRadius=windowRadius, **kwargs)

    def apply_sorting(self, obj_list, options=None):
        return sorted(obj_list, key=lambda msg: msg.distance)

    def obj_get_list(self, bundle, **kwargs):
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']
        windowRadius = kwargs['windowRadius']

        def distance(message):
            def distance_between(lat1, lon1, lat2, lon2):
                """
                Distance between two coordinates given in angles. Algorithm taken from:
                http://www.movable-type.co.uk/scripts/latlong.html
                """
                R = 6371 # km
                dLat = math.radians(lat2 - lat1)
                dLon = math.radians(lon2 - lon1)
                lat1 = math.radians(lat1)
                lat2 = math.radians(lat2)

                a = math.sin(dLat/2)**2 + math.sin(dLon/2)**2 * math.cos(lat1) * math.cos(lat2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return R * c * 1000 # return amount of meters.

            def distance_to(location):
                return distance_between(latitude, longitude, location[0], location[1])

            return distance_to((message.location_lat, message.location_lon))

        messages = super(MessageResource, self).obj_get_list(bundle, **kwargs)
        for message in messages:
            message.distance = distance(message)

        messages = filter(lambda msg: msg.distance <= windowRadius, messages)
        return messages

    def obj_create(self, bundle, **kwargs):
        user = User.objects.get(id=bundle.data['user_id'])

        if bundle.data['expires']:
            msg = Message(
                user = user,
                text = bundle.data['text'],
                location_lat = bundle.data['location_lat'],
                location_lon = bundle.data['location_lon'],
                radius = bundle.data['radius'],
                expires = bundle.data['expires']
            )
        else:
            msg = Message(
                user = user,
                text = bundle.data['text'],
                location_lat = bundle.data['location_lat'],
                location_lon = bundle.data['location_lon'],
                radius = bundle.data['radius']
            )           

        msg.save()

        return msg
