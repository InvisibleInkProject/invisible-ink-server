from django.conf.urls import patterns, include, url
from django.contrib import admin

from inks.resources import MessageResource, UserResource, RegisterResource

from tastypie.api import Api

import inks.models

admin.autodiscover()

api = Api(api_name='v1')    
api.register(MessageResource())
api.register(UserResource())
api.register(RegisterResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^api/', include(api.urls)),

    #Add the oauth2 urls
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
