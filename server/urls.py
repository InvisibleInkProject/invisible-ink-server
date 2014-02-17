from django.conf.urls import patterns, include, url
from django.contrib import admin
from inks.resources import MessageResource
from tastypie.api import Api

import inks.models

admin.autodiscover()

api = Api(api_name='v1')    
api.register(MessageResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^api/', include(api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
