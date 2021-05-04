from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from notice.models import Comment
from notice.serializers import CommentSerializer
from utils.permissions import ActionBasedPermission, IsMine


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'create'],
        IsMine : ['update', 'partial_update', 'destroy', ],
        IsAdminUser: ['list', 'update', 'partial_update', 'destroy', ],
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)