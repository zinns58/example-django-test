import os
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, password, nickname):

        if not username:
            raise ValueError('must have username')

        user = self.model(
            username=username,
            nickname=nickname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, username, password, nickname):
        user = self.create_user(
            username=username,
            password=password,
            nickname=nickname
        )

        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, nickname):
        user = self.create_user(
            username=username,
            password=password,
            nickname=nickname
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    # field
    username = models.EmailField(max_length=128, unique=True, verbose_name='이메일')
    password = models.CharField(max_length=100, verbose_name='비밀번호')
    nickname = models.CharField(max_length=30, verbose_name='닉네임')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    leave_date = models.DateTimeField(blank=True, null=True, verbose_name='탈퇴일')
    create_date = models.DateTimeField(default=timezone.now, verbose_name='가입일')

    # 커스텀 모델 매니져 UserManager 사용
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'nickname',
    ]

    # 생성일 순으로 정렬
    class Meta:
        ordering = ('-id',)
        verbose_name = 'user'
        verbose_name_plural = 'user'

    def __str__(self):
        return 'username: {}, nickname: {}'.format(self.username, self.nickname)