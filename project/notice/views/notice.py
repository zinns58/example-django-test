from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from notice.models import Notice, Comment
from notice.serializers import NoticeListSerializer, NoticeSerializer, CommentSerializer
from utils.permissions import IsStaff


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        elif self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [IsStaff, ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return NoticeListSerializer
        else:
            return NoticeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    