from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class InkAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list

    def read_detail(self, object_list, bundle):
        return True


    def create_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        print 'create_list'
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def update_list(self, object_list, bundle):
        print 'update_list'
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
