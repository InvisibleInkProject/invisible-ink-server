from django.conf.urls import patterns, include, url
from django.contrib import admin
from ink.resources import MessageResource
from ink.views import GetByLocationView
from tastypie.api import Api

import ink.models

admin.autodiscover()
admin.site.register(ink.models.Message)
admin.site.register(ink.models.User)

api = Api(api_name='v1')    
api.register(MessageResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^twitter/$', GetByLocationView.as_view(), name='home'),
    url(r'^api/', include(api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
