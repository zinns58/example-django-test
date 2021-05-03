from django.contrib import admin
from member.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'nickname',
    )

    list_display_links = (
        'username',
        'nickname',
    )
