from django.contrib.auth import get_user_model
from rest_framework import serializers

from notice.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment

        fields = [
            'author',
            'content',
            'notice',
            'create_date',
        ]

        read_only_fields = [
            'author',
            'notice',
            'create_date',
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment

        fields = [
            'author',
            'content',
            'notice',
            'create_date',
        ]

        read_only_fields = [
            'author',
            'create_date',
        ]
