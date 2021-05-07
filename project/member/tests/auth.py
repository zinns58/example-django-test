from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from member.serializers import UserSerializer
UserModel = get_user_model()


class AuthTestCase(TestCase):
    
    def setUp(self):
        """
        set up testcase data
        """

        self.client = APIClient()

        self.test_user = UserModel.objects.create_superuser(
            username='admin001@gmail.com',
            password='qwe123',
            nickname='admin001'
        )
        self.token, _ = Token.objects.get_or_create(user=self.test_user)

    def test_api_token_login(self):
        """
        test token login
        """

        test_user_token = {
            'token': self.token.key
        }
        self.response = self.client.post(
            reverse('member:login'),
            test_user_token,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_logout(self):
        """
        test logout
        """

        self.client.force_authenticate(user=self.test_user)
        self.response = self.client.post(
            reverse('member:logout'),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)