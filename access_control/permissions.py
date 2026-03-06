from rest_framework.permissions import BasePermission

from .services import user_has_access


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return user_has_access(request.user, 'access_rules', 'manage')
