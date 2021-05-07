from django.contrib.auth import get_user_model
from rest_framework import serializers

from notice.models import Notice
from notice.serializers import CommentSerializer

class NoticeListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notice

        fields = [
            'author',
            'title',
            'content',
            'create_date',
        ]

        read_only_fields = [
            'author',
            'create_date',
        ]

class NoticeSerializer(serializers.ModelSerializer):

    notice_comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Notice

        fields = [
            'author',
            'title',
            'content',
            'notice_comment',
            'create_date',
        ]

        read_only_fields = [
            'author',
            'create_date',
        ]