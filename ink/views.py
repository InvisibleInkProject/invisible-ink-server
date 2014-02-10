"""
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.generic import TemplateView
from ink.models import Message

import json
import settings
import twitter

class GetByLocationView(TemplateView):
    def get(self, request):
        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY, 
                consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                access_token_key=settings.TWITTER_ACCESS_KEY,
                access_token_secret=settings.TWITTER_ACCESS_SECRET)

        test_geocode = (52.92, 10.70, '1km')
        result = api.GetSearch(geocode=test_geocode)

        return HttpResponse(map(str, map(self._twitter2msg, result)))
    
    def _twitter2msg(self, twitter_status):
        location = twitter_status.geo or twitter_status.location or twitter_status.coordinates

        if location is None:
            return None

        location_split = location.split(',') # Hopefully it's formatted like this: { "geo" : "+13.37,-142.03" }, but if it isn't, FIXME here.
        location_lat = float(location_split[0])
        location_lon = float(location_split[1])

        return Message(text=twitter_status.text,
            created=twitter_status.created_at,
            location_lat=location_lat,
            location_lon=location_lon,
        )
"""