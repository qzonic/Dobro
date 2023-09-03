from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """ Permission that allow modifying object only by creator. """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
