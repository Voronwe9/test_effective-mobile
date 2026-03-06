from rest_framework.routers import DefaultRouter

from .views import ActionViewSet, ResourceViewSet, RolePermissionViewSet, RoleViewSet, UserRoleViewSet

router = DefaultRouter()
router.register('roles', RoleViewSet)
router.register('actions', ActionViewSet)
router.register('resources', ResourceViewSet)
router.register('permissions', RolePermissionViewSet)
router.register('user-roles', UserRoleViewSet)

urlpatterns = router.urls
