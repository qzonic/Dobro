from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Permission that allow modifying object only by creator. """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
