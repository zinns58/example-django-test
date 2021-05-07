from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from member.serializers import UserSerializer
UserModel = get_user_model()


class UserTestCase(TestCase):
    
    def setUp(self):
        """
        set up testcase data
        """

        # initialize client
        self.client = APIClient()

        # create test user
        self.test_user = UserModel.objects.create_superuser(
            username='admin001@gmail.com',
            password='qwe123',
            nickname='admin001'
        )

        # force authentication
        self.client.force_authenticate(user=self.test_user)

    def test_api_create_member(self):
        """
        test create member
        """

        new_data = {
            'username': 'testuser2@gmail.com', 
            'password': 'testuser2',
            'nickname': 'testuser2'
            }
        self.response = self.client.post(
            reverse('member:create'),
            new_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_get_member(self):
        """
        test get member
        """

        # get data from db
        user = UserModel.objects.all().first()
        user_serializer = UserSerializer(user, many=False)

        # get API response
        self.response = self.client.get(
            reverse('member:detail', kwargs={'pk': user.id}),
            format='json'
        )        
        self.assertEqual(self.response.data, user_serializer.data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_member(self):
        """
        test update member
        """

        # get data from default
        test_user_id = self.test_user.id
        change_user = {
            'nickname': 'changer1'
        }

        # update data
        self.response = self.client.put(
            reverse('member:update', kwargs={'pk': test_user_id}),
            change_user,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_delete_member(self):
        """
        test delete member
        """

        # get data from default
        test_user_id = self.test_user.id

        # delete data
        self.response = self.client.delete(
            reverse('member:delete', kwargs={'pk': test_user_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)