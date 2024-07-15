from rest_framework import permissions


class ManagerPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return False

        if view.action == 'destroy':
            return False

        if view.action in ['update', 'partial_update']:
            return request.user and request.user.groups.filter(name='Manager').exists()

        if view.action in ['list', 'retrieve']:
            return True

        return False