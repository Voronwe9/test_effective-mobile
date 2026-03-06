from .models import RolePermission


def user_has_access(user, resource_code: str, action_code: str) -> bool:
    if not user.is_authenticated:
        return False

    return RolePermission.objects.filter(
        role__userrole__user=user,
        resource__code=resource_code,
        action__code=action_code,
        is_allowed=True,
    ).exists()
