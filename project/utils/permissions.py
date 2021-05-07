from rest_framework import permissions


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


class IsOwner(permissions.BasePermission):
    """
    내 소유가 아니면, 요청 거절
    """
    message = '권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    내 소유가 아니면, 보기만 가능
    """
    message = '권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsOwnerOrStaff(permissions.BasePermission):
    """
    내 소유이거나, 관리자 인 경우 허용
    """
    message = '권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True

        return obj.author == request.user
