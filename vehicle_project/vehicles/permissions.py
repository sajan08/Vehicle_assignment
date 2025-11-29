from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    """
    Permission matrix:
    - Super admin: all methods allowed
    - Admin: GET (list/retrieve), PUT, PATCH (edit) allowed
    - User: GET only
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_super_admin():
            return True

        method = request.method.upper()
        if user.is_admin():
            if method in ('GET', 'PUT', 'PATCH'):
                return True
            return False

        if user.is_user():
            return method in ('GET')

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
