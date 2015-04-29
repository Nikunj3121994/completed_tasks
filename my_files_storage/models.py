# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django import forms
from django.core.exceptions import PermissionDenied
try:
    from django.core.exceptions import AppRegistryNotReady
except ImportError:
    AppRegistryNotReady = Exception
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
# from utils import bind_delete_update_file

try:
    MAX_USER_FILES_COUNT = settings.MAX_USER_FILES_COUNT
except AttributeError:
    MAX_USER_FILES_COUNT = 100

logger = logging.getLogger(__name__)

APP_LABEL = 'my_files_storage'


try:
    USER_MODEL = get_user_model()
except AppRegistryNotReady, err:
    logger.debug(err)
    USER_MODEL = User
except Exception, err:
    logger.error(err)
    USER_MODEL = User


logger = logging.getLogger(__name__)


class File(models.Model):
    hash = models.CharField(
        max_length=255, unique=True, blank=True, verbose_name=_('хэш'))
    file = models.FileField(
        max_length=256, upload_to='%Y/%m/%d', verbose_name=_('путь'))
    user = models.ManyToManyField(
        to=USER_MODEL, through='UserFile', related_name='files', verbose_name=_('пользователь'))
    # user = models.ManyToManyField(to=USER_MODEL, related_name='files', verbose_name =_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('файл')
        verbose_name_plural = _('файлы')

    def __unicode__(self):
        return '%s' % self.file.name.split('/')[-1]


class UserFile(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('имя'))
    file = models.ForeignKey(
        File, related_name='userfiles', verbose_name=_('файл'))
    user = models.ForeignKey(
        User,  related_name='userfiles', verbose_name=_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('пользовательский файл')
        verbose_name_plural = _('пользовательские файлы')

    def __unicode__(self):
        return '%s' % self.title


# Биндим сигналы на удаление и обновление файлов
@receiver(pre_save, sender=File)
def create_hash(instance, *args, **kwargs):
    logger.debug(instance)
    file = instance.file.file
    import hashlib
    m = hashlib.md5()
    while True:
        data = file.read(8000)
        if not data:
            break
        m.update(data)
    logger.debug(m.hexdigest())
    instance.hash = m.hexdigest()
    older_file = File.objects.filter(hash=instance.hash)
    if older_file:
        raise IntegrityError('object already: _pk_ %s' % older_file.first().pk)
    return instance


@receiver(post_delete, sender=File)
def remove_files(instance, **kwargs):
    logger.debug(instance)
    for field in instance._meta.fields:
        if not isinstance(field, models.FileField):
            continue
        file_to_delete = getattr(instance, field.name)
        storage = file_to_delete.storage
        if file_to_delete and storage and storage.exists(file_to_delete.name):
            try:
                storage.delete(file_to_delete.name)
            except Exception:
                logger.exception(
                    "Unexpected exception while attempting to delete file '%s'" % file_to_delete.name)


@receiver(post_delete, sender=UserFile)
@receiver(pre_save, sender=UserFile)
def change_count_link(instance, signal, *args, **kwargs):
    logger.debug(instance)

    if signal is pre_save:
        user_files_count = UserFile.objects.filter(user=instance.user).count()
        logger.debug(user_files_count)
        if user_files_count >= MAX_USER_FILES_COUNT:
            logger.debug('so many users files')
            raise PermissionDenied('You have so many files %s!!! You can have %s' % (
                user_files_count, settings.MAX_USER_FILES_COUNT))

    if signal is post_delete:
        try:
            file = instance.file
        except ObjectDoesNotExist, err:
            logger.error(err)
            file = None
        if file:
            files_link_count = UserFile.objects.filter(file=file).count()
            logger.debug(files_link_count)
            if files_link_count == 0:
                logger.debug('need to delete files')
                # File.object
                logger.debug(instance.file)
                instance.file.delete()
    return
