from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User profile Serializer
    """

    class Meta:
        model = UserModel

        fields = (
            'id',
            'username',
            'nickname',
            'create_date',
        )

        read_only_fields = (
            'username',
            'create_date',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel

        fields = (
            'id',
            'username',
            'password',
            'nickname',
        )

        read_only_fields = (
            'create_date',
        )


    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data
        }

        return data