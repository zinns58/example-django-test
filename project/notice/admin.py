from django.contrib import admin
from notice.models import Notice, Comment


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'title',
        'content',
        'create_date'
    )

    link_display = (
        'id',
        'title'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'content',
        'create_date'
    )

    link_display = (
        'id',
    )