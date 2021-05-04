from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

UserModel = get_user_model()

class Notice(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return 'author : {}, title: {}, content: {}'.format(self.author, self.title, self.content)