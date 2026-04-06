from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    message = 'Only for Owner'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        return False
