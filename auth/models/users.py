# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.dispatch import receiver
from django.conf import settings
from ..managers import UserManager
from ..choices import USER_ROLES
from .roles import Role
from .groups import Group


APP_LABEL = 'protokol_auth'


class User(AbstractBaseUser):
    """
    Пользователь.
    Роли пользователей - это группы django.contrib.auth.models.Group
    У роли "Оператор" pk = 1
    У роли "Администратор" pk = 2
    У роли "Администратор безопасности" pk=3
    """
    username = models.CharField(max_length=255, unique=True, verbose_name='имя пользователя')
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='дата оформления', editable=False)
    last_name = models.CharField(max_length=300, verbose_name='фамилия')
    first_name = models.CharField(max_length=300, verbose_name='имя')
    middle_name = models.CharField(max_length=300, verbose_name='отчество')
    desktop_url = models.CharField(max_length=300, verbose_name='URL для ручной обработки', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'middle_name']

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ('username',)

    def __unicode__(self):
        return self.get_full_name()

    @property
    def is_superuser(self):
        return False

    @property
    def is_staff(self):
        if self.is_active:
            return self.is_superuser
        return False

    @property
    def is_operator(self):
        return self.is_in_roles([USER_ROLES.OPERATOR])

    @property
    def is_admin(self):
        return self.is_in_roles([USER_ROLES.ADMINISTRATOR])

    @property
    def is_security_admin(self):
        return self.is_in_roles([USER_ROLES.SECURITY_ADMIN])

    def get_full_name(self):
        """
        Полное имя пользователя.
        """
        return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    def get_short_name(self):
        """
        Краткое имя пользователя.
        """
        return self.username

    def get_all_permissions(self, obj=None):
        if self.is_active:
            return super(User, self).get_all_permissions(obj)
        return set()

    def block(self, commit=True):
        self.is_active = False
        if commit:
            self.save()
        return self

    def unblock(self, commit=True):
        self.is_active = True
        if commit:
            self.save()
        return self

    @property
    def can_be_blocked(self):
        return self.is_active

    @property
    def can_be_unblocked(self):
        return not self.is_active

    _cached_roles = None

    def is_in_roles(self, roles):
        if not roles:
            return False
        for role in self.get_roles():
            if role.pk in roles:
                return True
        return False

    def get_roles(self):
        if self._cached_roles is None:
            #role_model = get_model('django_ldap_groups', 'LDAPRole')
            self._cached_roles = Role.objects.filter(groups=self.groups.all()).distinct()
        return self._cached_roles


if settings.PROTOCOL_AUTH_WITH_LDAP:
    from django_auth_ldap.backend import LDAPBackend, populate_user

    @receiver(populate_user, sender=LDAPBackend)
    def set_user_data(sender, **kwargs):
        user = kwargs['user']
        ldap_user = kwargs['ldap_user']
        user_changed = False
        # подстановка ФИО из свойства сn
        name_list = ldap_user.attrs.get('cn', None)
        if name_list:
            name_list = name_list[0].split(' ')
        if name_list and len(name_list) == 3:
            if user.first_name != name_list[1]:
                user.first_name = name_list[1]
                user_changed = True
            if user.middle_name != name_list[2]:
                user.middle_name = name_list[2]
                user_changed = True
            if user.last_name != name_list[0]:
                user.last_name = name_list[0]
                user_changed = True
        else:
            user.last_name = user.username
            user.first_name = user.username
            user.middle_name = user.username
        # # поля ФИО - обязательные, если они пустые, то подставляется логин
        # if not user.first_name:
        #     user.first_name = user.username
        #     user_changed = True
        # if not user.middle_name:
        #     user.first_name = user.username
        #     user_changed = True
        # if not user.last_name:
        #     user.first_name = user.username
        #     user_changed = True
        if user_changed:
            user.save()
        # Синхронизация групп
        sync_group_names = set(ldap_user.group_names)
        groups = user.groups.all()
        user_group_names = set()
        # Удаление пользователя из групп
        for group in groups:
            if group.name in sync_group_names:
                user_group_names.add(group.name)
            else:
                user.groups.remove(group)
        # Добавление пользователя в группы
        new_group_names = sync_group_names.difference(user_group_names)
        for name in new_group_names:
            try:
                group = Group.objects.get(name=name)
            except Group.DoesNotExist:
                group = Group(name=name)
                group.save()
            user.groups.add(group)
