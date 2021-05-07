from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet

from notice.models import Comment
from notice.serializers import CommentSerializer, CommentCreateSerializer
from utils.permissions import IsStaff, IsOwnerOrStaff


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsStaff, ]
        elif self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [IsOwnerOrStaff]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)