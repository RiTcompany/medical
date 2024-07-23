from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.request import HttpRequest

class IsManagerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'PATCH':
            return True if request.user and request.user.groups.filter(name='Manager').exists() else False
        return False

class IsSubscriberUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if request.parser_context['kwargs']['pk'] > 100:
                return request.user and request.user.groups.filter(name='Subscriber').exists()
            return True

        return False