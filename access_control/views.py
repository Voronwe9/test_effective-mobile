from rest_framework import viewsets

from .models import Action, Resource, Role, RolePermission, UserRole
from .permissions import IsAdminRole
from .serializers import (
    ActionSerializer,
    ResourceSerializer,
    RolePermissionSerializer,
    RoleSerializer,
    UserRoleSerializer,
)


class AdminManagedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]


class RoleViewSet(AdminManagedModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ActionViewSet(AdminManagedModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ResourceViewSet(AdminManagedModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class RolePermissionViewSet(AdminManagedModelViewSet):
    queryset = RolePermission.objects.select_related('role', 'action', 'resource').all()
    serializer_class = RolePermissionSerializer


class UserRoleViewSet(AdminManagedModelViewSet):
    queryset = UserRole.objects.select_related('user', 'role').all()
    serializer_class = UserRoleSerializer
