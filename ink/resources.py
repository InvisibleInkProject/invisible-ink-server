from ink.models import Message
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        authorization = Authorization() #TODO
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get' ]
