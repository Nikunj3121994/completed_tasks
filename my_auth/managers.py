# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager


class UserManager(DjangoBaseUserManager):
    """
    Менеджер модели пользователя.
    """

    # TODO: использовать форму ?
    def create_user(self, username, password=None, **extra_fields):
        """
        Создание нового пользователя.
        """
        now = timezone.now()
        if not username:
            raise ValueError('Username must be set')
        user = self.model(username=username, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Создание нового суперпользователя.
        """
        u = self.create_user(username, password, **extra_fields)
        #u.is_superuser = True
        u.save(using=self._db)
        return u
