#Imports
import json
import logging
import math

#Django imports
from django.conf.urls import url
from django.http import HttpResponse
from django.views.generic import View

#Third party imports
from tastypie import fields, http
from tastypie.exceptions import NotFound, ImmediateHttpResponse
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication
from authentication import OAuth20Authentication
from authorization import InkAuthorization, RegisterAuthorization

#Ink imports
from inks.models import Message, User
from inks.serializers import InksSerializer

from provider.oauth2.models import Client

class MessageResource(ModelResource):
    distance = fields.FloatField(attribute='distance', blank=True, null=True)

    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]

        authentication = OAuth20Authentication()
        #authorization = InkAuthorization()
        serializer = InksSerializer(['json'])

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>{})/(?P<latitude>([\+-]?\d+\.\d+)),(?P<longitude>([\+-]?\d+\.\d+)),(?P<windowRadius>([\+-]?\d+\.\d+))/$".format(self._meta.resource_name), self.wrap_view('dispatch_list_with_geo'), name="api_dispatch_list_with_geo"),
        ]

    def dispatch_list_with_geo(self, request, latitude, longitude, windowRadius, **kwargs):

        self.check_for_array_only_param(request)

        latitude = float(latitude)
        longitude = float(longitude)
        windowRadius = float(windowRadius)

        return self.dispatch_list(request, latitude=latitude, longitude=longitude, windowRadius=windowRadius, **kwargs)

    """
    TODO: This is probably not the best thing to do since for every request
          we now change the meta object. Perhaps some performance testing can be done
          to ensure that this is not a problem
    """
    def check_for_array_only_param(self, request):
        self.Meta.serializer.no_meta = False
        if request.GET.get('no_meta') == 'true':
            self.Meta.serializer.no_meta = True

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
                R = 6371
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
    
    # Todo: Check if this is the right way to do this and also check
    #       why the authorization isn't called            
    def obj_create(self, bundle, **kwargs):

        #Check if the user is authorized to create
        self.authorized_create_detail(Message.objects.all(), bundle)

        #TODO: Check what this does exactly
        self.is_valid(bundle)

        if bundle.errors:
            self.error_response(bundle.errors, request)

        #Get the user_id from the request
        user_id = bundle.request.user.id
        user = User.objects.get(id=user_id)

        msg = Message(
            user = user,
            text = bundle.data['text'],
            location_lat = bundle.data['location_lat'],
            location_lon = bundle.data['location_lon'],
            radius = bundle.data['radius']
        )

        msg.save()

        return msg
    """
    def alter_list_data_to_serialize(self,request,data_dict): 
        if isinstance(data_dict,dict): 
            if 'meta' in data_dict: 
                del(data_dict['meta']) 
                return data_dict  

    def dehydrate(self, bundle):
        print bundle
        return {}
    """


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]
        excludes = ['password']
        authentication = OAuth20Authentication()
        authorization = InkAuthorization()

class RegisterResource(ModelResource): 
    class Meta:
        queryset = Client.objects.all()
        resource_name = 'register'
        list_allowed_methods = [ 'post' ]
        detail_allowed_methods = []
        authentication = Authentication()
        authorization = RegisterAuthorization()
        always_return_data = True
        fields = ['client_id', 'client_secret']
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):
        #TODO:  Make sure that both users are created and then return 
        # else loop it back
        #TODO: Create more json friendly error messages
        try:
            user = User(
                username = bundle.data['username'],
                email = bundle.data['email'],
                birthday = bundle.data['birthday']
            )
            user.set_password(bundle.data['password'])
            user.save()
        except KeyError, e:
            raise ImmediateHttpResponse(response=http.HttpBadRequest(e))
        except Exception, e:
            raise ImmediateHttpResponse(response=http.HttpBadRequest(e))

        # Reset the bundle data so that the passed in data does not get returned
        bundle.data = {}

        #Set the client as the object to be returned
        bundle.obj = Client.objects.get(user=user)

        return bundle
