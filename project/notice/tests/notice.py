from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from notice.models import Notice
from notice.serializers import NoticeSerializer
UserModel = get_user_model()


class NoticeTestCase(TestCase):
    
    def setUp(self):
        """
        set up testcase data
        """

        # initialize client
        self.client = APIClient()

        # create admin user
        self.admin_user = UserModel.objects.create_superuser(
            username='admin001@gmail.com',
            password='qwe123',
            nickname='admin001'
        )

        # create test user
        self.test_user = UserModel.objects.create_user(
            username='test001@gmail.com',
            password='qwe123',
            nickname='test001'
        )

        # create default notice
        self.notice = Notice.objects.create(
            title='notice to everyone',
            content='nice to meet your friends',
            author=self.admin_user
        )
        
    def test_api_get_notice_list(self):
        """
        test get notice list
        """

        # get API response
        self.response = self.client.get(
            reverse('notice-list'),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_create_notice_by_admin(self):
        """
        test create notice by admin
        """

        new_data = {
            'title': 'new notice',
            'content': 'new content'
            }

        # authentication admin
        self.client.force_authenticate(user=self.admin_user)
        
        self.response = self.client.post(
            reverse('notice-list'),
            new_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_create_notice_by_user(self):
        """
        test create notice by admin
        """

        new_data = {
            'title': 'new notice',
            'content': 'new content'
            }

        # authentication admin
        self.client.force_authenticate(user=self.test_user)
        
        self.response = self.client.post(
            reverse('notice-list'),
            new_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_create_notice_by_anonymous(self):
        """
        test create notice by anonymous
        """

        new_data = {
            'title': 'new notice',
            'content': 'new content'
            }

        self.response = self.client.post(
            reverse('notice-list'),
            new_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_notice_detail(self):
        """
        test notice detail
        """

        # get data from db
        notice = Notice.objects.all().first()
        notice_serializer = NoticeSerializer(notice, many=False)

        # get API response
        self.response = self.client.get(
            reverse('notice-detail', kwargs={'pk': notice.id}),
            format='json'
        )
        self.assertEqual(self.response.data, notice_serializer.data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_notice_by_admin(self):
        """
        test update notice by admin
        """

        # get data from default
        notice_id = self.notice.id
        change_notice = {
            'title': 'change notice title',
            'content': 'change notice content'
        }
        # authentication admin
        self.client.force_authenticate(user=self.admin_user)

        # update data
        self.response = self.client.put(
            reverse('notice-detail', kwargs={'pk': notice_id}),
            change_notice,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_notice_by_user(self):
        """
        test update notice by user
        """

        # get data from default
        notice_id = self.notice.id
        change_notice = {
            'title': 'change notice title',
            'content': 'change notice content'
        }

        # authentication user
        self.client.force_authenticate(user=self.test_user)

        # update data
        self.response = self.client.put(
            reverse('notice-detail', kwargs={'pk': notice_id}),
            change_notice,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_update_notice_by_anonymous(self):
        """
        test update notice by anonymous
        """

        # get data from default
        notice_id = self.notice.id
        change_notice = {
            'title': 'change notice title',
            'content': 'change notice content'
        }

        # update data
        self.response = self.client.put(
            reverse('notice-detail', kwargs={'pk': notice_id}),
            change_notice,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_delete_notice_by_admin(self):
        """
        test delete notice by admin
        """

        # get data from default
        notice_id = self.notice.id

        # authentication admin
        self.client.force_authenticate(user=self.admin_user)

        # delete data
        self.response = self.client.delete(
            reverse('notice-detail', kwargs={'pk': notice_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_delete_notice_by_user(self):
        """
        test delete notice by user
        """

        # get data from default
        notice_id = self.notice.id

        # authentication user
        self.client.force_authenticate(user=self.test_user)

        # delete data
        self.response = self.client.delete(
            reverse('notice-detail', kwargs={'pk': notice_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_api_delete_notice_by_anonymous(self):
        """
        test delete notice by anonymous
        """

        # get data from default
        notice_id = self.notice.id

        # delete data
        self.response = self.client.delete(
            reverse('notice-detail', kwargs={'pk': notice_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)