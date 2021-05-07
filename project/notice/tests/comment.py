from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from notice.models import Notice, Comment
from notice.serializers import NoticeSerializer, CommentSerializer
UserModel = get_user_model()


class CommentTestCase(TestCase):
    
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

        self.test_user_002 = UserModel.objects.create_user(
            username='test002@gmail.com',
            password='qwe123',
            nickname='test002'
        )

        # create default notice
        self.notice = Notice.objects.create(
            title='notice to everyone',
            content='nice to meet your friends',
            author=self.admin_user
        )

        # create default comment
        self.comment = Comment.objects.create(
            content='good comment',
            notice=self.notice,
            author=self.test_user
        )
        
    def test_api_get_comment_list_by_admin(self):
        """
        test get comment list by admin
        """

        # authentication admin  
        self.client.force_authenticate(user=self.admin_user)

        # get API response
        self.response = self.client.get(
            reverse('comment-list'),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_get_comment_list_by_user(self):
        """
        test get comment list by user
        """

        # authentication admin  
        self.client.force_authenticate(user=self.test_user)
        
        # get API response
        self.response = self.client.get(
            reverse('comment-list'),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_comment_list_by_anonymous(self):
        """
        test get comment list by anonymous
        """
        
        # get API response
        self.response = self.client.get(
            reverse('comment-list'),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_create_comment_by_user(self):
        """
        test create comment by user
        """

        # get data from default
        notice_id = self.notice.id
        new_data = {
            'content': 'new comment!!',
            'notice': notice_id
        }
        # authentication user
        self.client.force_authenticate(user=self.test_user)

        # get API response
        self.response = self.client.post(
            reverse('comment-list'),
            new_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_create_comment_by_anonymous(self):
        """
        test create comment by anonymous
        """

        # get data from default
        notice_id = self.notice.id
        new_data = {
            'content': 'new comment!!',
            'notice': notice_id
        }
        # get API response
        self.response = self.client.post(
            reverse('comment-list'),
            new_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_comment_detail(self):
        """
        test comment detail
        """

        # get data from db
        comment = Comment.objects.all().first()
        comment_serializer = CommentSerializer(comment, many=False)

        # get API response
        self.response = self.client.get(
            reverse('comment-detail', kwargs={'pk': comment.id}),
            format='json'
        )
        self.assertEqual(self.response.data, comment_serializer.data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_comment_by_admin(self):
        """
        test update comment by admin
        """

        # get data from default
        comment_id = self.comment.id
        change_data = {
            'content': 'change comment content'
        }
        # authentication admin
        self.client.force_authenticate(user=self.admin_user)

        # update data
        self.response = self.client.put(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            change_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_comment_by_auth_user(self):
        """
        test update comment by auth user(is mine)
        """

        # get data from default
        comment_id = self.comment.id
        change_data = {
            'content': 'change comment content'
        }
        # authentication test_user
        self.client.force_authenticate(user=self.test_user)

        # update data
        self.response = self.client.put(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            change_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_comment_by_other_user(self):
        """
        test update comment by othery user(is not mine)
        """

        # get data from default
        comment_id = self.comment.id
        change_data = {
            'content': 'change comment content'
        }
        # authentication test_user_002
        self.client.force_authenticate(user=self.test_user_002)

        # update data
        self.response = self.client.put(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            change_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_update_comment_by_other_anonymous(self):
        """
        test update comment by anonymous
        """

        # get data from default
        comment_id = self.comment.id
        change_data = {
            'content': 'change comment content'
        }
        # update data
        self.response = self.client.put(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            change_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_delete_comment_by_admin(self):
        """
        test delete comment by admin
        """

        # get data from default
        comment_id = self.comment.id

        # authentication admin
        self.client.force_authenticate(user=self.admin_user)

        # delete data
        self.response = self.client.delete(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_delete_comment_by_auth_user(self):
        """
        test delete comment by auth user
        """

        # get data from default
        comment_id = self.comment.id

        # authentication user
        self.client.force_authenticate(user=self.test_user)

        # delete data
        self.response = self.client.delete(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_delete_comment_by_other_user(self):
        """
        test delete comment by other user
        """

        # get data from default
        comment_id = self.comment.id

        # authentication user
        self.client.force_authenticate(user=self.test_user_002)

        # delete data
        self.response = self.client.delete(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_api_delete_comment_by_anonymous(self):
        """
        test delete comment by anonymous
        """

        # get data from default
        comment_id = self.comment.id

        # delete data
        self.response = self.client.delete(
            reverse('comment-detail', kwargs={'pk': comment_id}),
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)