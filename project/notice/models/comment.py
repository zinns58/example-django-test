from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from notice.models import Notice
UserModel = get_user_model()

class Comment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='notice_comment')
    content = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return 'author : {}, notice: {}, content: {}'.format(self.author, self.notice, self.content)