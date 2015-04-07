# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import AppRegistryNotReady
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from utils import bind_delete_update_file


logger = logging.getLogger(__name__)

APP_LABEL = 'users_files'


try:
    USER_MODEL = get_user_model()
except AppRegistryNotReady,err:
    logger.debug(err)
    USER_MODEL = User
except Exception,err:
    logger.error(err)
    USER_MODEL = User


logger = logging.getLogger(__name__)



class File(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('имя'))
    hash = models.CharField(max_length=255, unique=True, primary_key=True, verbose_name=_('хэш'))
    path = models.FileField(max_length=256, blank=True, upload_to="%Y/%m/%d", verbose_name=_('путь'))
    count_link = models.PositiveSmallIntegerField(verbose_name=_('количество ссылок'))
    user = models.ManyToManyField(to=USER_MODEL, related_name='files', verbose_name =_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('файл')
        verbose_name_plural = _('файлы')

    def __unicode__(self):
        return '%s' % self.title


# class User_file(User):
#     files = models.ForeignKey('File', related_name='users', verbose_name=_('файл'))
#     user = models.ForeignKey(User, verbose_name='Пользователь', blank=True, null=True, related_name='folders_al')
#
#     class Meta:
#         app_label = APP_LABEL
#         verbose_name = _('пользователь')
#         verbose_name_plural = _('пользователи')
#
#     def __unicode__(self):
#         return '%s' % self.username

    # def get_file_name(self):
    #     try:
    #         return self.basename
    #         # if self.basename:
    #         #     return self.basename
    #         # return self.file_path.name
    #     except:
    #         return None
# @receiver(post_save, sender=Task)
# def change_task_status(instance, *args, **kwargs):
#     if not instance.pk:
#         return
#     if instance.finish_time:
#         status_code = instance.get_task_status()
#         if status_code.code != StatusType.STATUS_TYPES.RUNNING:
#             instance.save()

#Биндим сигналы на удаление и обновление файлов
bind_delete_update_file([File,])

# @receiver(post_save, sender=User_file)
# def change_task_status(instance, *args, **kwargs):
#     if not instance.pk:
#         return
    # if instance.finish_time:
    #     status_code = instance.get_task_status()
    #     if status_code.code != StatusType.STATUS_TYPES.RUNNING:
    #         instance.save()