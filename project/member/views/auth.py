from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer
UserModel = get_user_model()


class TokenLoginView(APIView):
    """
    토큰으로 로그인
    """

    permission_classes = []

    def post(self, request):
        r_token = request.data.get('token', None)

        if not r_token:
            return Response({'detail': '토큰이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.filter(key=r_token).first()
        if not token:
            return Response({'detail': '토큰이 유효하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        user = UserModel.objects.filter(id=token.user_id).first()
        if not user:
            return Response({'detail': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)

        user.update_date = timezone.now()
        user.save()

        user_serializer = UserSerializer(user, context={'request': request})
        context = {
            'token': token.key,
            'user': user_serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    사용자 로그아웃
    """

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        r_user = request.user
        user = UserModel.objects.filter(id=r_user.id).first()
        if not user:
            return Response({'detail': '존재하지 않는 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request.user.auth_token.delete()
        except Exception as error:
            message = '{}'.format(error)
            return Response({'detail': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': 'ok'}, status=status.HTTP_200_OK)
