from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from notice.models import Notice, Comment
from notice.serializers import NoticeListSerializer, NoticeSerializer, CommentSerializer
from utils.permissions import ActionBasedPermission, IsMine


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['create', 'update', 'partial_update', 'destroy', ],
        AllowAny: ['list', 'retrieve', ],
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return NoticeListSerializer
        else:
            return NoticeSerializer