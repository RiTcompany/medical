from rest_framework import permissions


class IsSubscriberUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if request.parser_context['kwargs']['pk'] > 100:
                return request.user and request.user.groups.filter(name='Subscriber').exists()
            return True

        return False