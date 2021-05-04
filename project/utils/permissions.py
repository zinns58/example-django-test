from rest_framework import permissions
from rest_framework.permissions import AllowAny


class ActionBasedPermission(AllowAny):
    """
    request action permission
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class IsSuperUser(permissions.BasePermission):
    """
    슈퍼 유저 권한 체크
    """

    message = '권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class IsStaff(permissions.BasePermission):
    """
    스테프 권한 체크
    """

    message = '권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        return user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    내 소유가 아니면, 보기만 가능
    """
    message = '권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user


class IsMine(permissions.BasePermission):
    """
    내 소유가 아니면, 요청 거절
    """
    message = '권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
