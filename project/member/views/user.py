from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from member.serializers import UserSerializer, UserCreateSerializer
UserModel = get_user_model()


class IsMine(permissions.BasePermission):
    message = '권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        return user == view.get_object()


class UserCreateView(APIView):

    """
    사용자 생성하기
    """

    permission_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = serializer.save()
        except Exception as error:
            message = '{}'.format(error)
            return Response({'detail': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=result, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    사용자 상세/업데이트/삭제
    """

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsMine,
    )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = UserCreateSerializer
            return serializer_class
        else:
            serializer_class = UserSerializer
            return serializer_class
