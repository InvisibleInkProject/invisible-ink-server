from django.conf.urls import patterns, include, url
from django.contrib import admin
from ink.resources import MessageResource, UserResource
#from ink.views import GetByLocationView
from tastypie.api import Api

import ink.models

admin.autodiscover()
#admin.site.register(ink.models.Message)
#admin.site.register(ink.models.User)

api = Api(api_name='v1')    
api.register(MessageResource())
api.register(UserResource())

urlpatterns = patterns('',
    # Examples:
#    url(r'^twitter/$', GetByLocationView.as_view(), name='home'),
    url(r'^api/', include(api.urls)),

    #Add the oauth2 urls
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
