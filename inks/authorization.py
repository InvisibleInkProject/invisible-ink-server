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
        raise Unauthorized("Sorry, no mass creates.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no mass updates.")

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
