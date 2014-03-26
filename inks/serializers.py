import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer

class InksSerializer(Serializer):

    no_meta = False

    def to_json(self, data, options=None):
        options = options or {}

        data = self.to_simple(data, options)

        #Use only the objects array and remove all the other stuff
        if data.has_key('objects') and self.no_meta:
            data = data['objects']

        return json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)
