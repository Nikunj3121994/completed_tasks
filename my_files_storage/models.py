# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
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
from utils import get_exif_dict

try:
    MAX_USER_FILES_COUNT = settings.MAX_USER_FILES_COUNT
except AttributeError:
    MAX_USER_FILES_COUNT = 0

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
    hash = models.CharField(max_length=255, unique=True, blank=True, verbose_name=_('хэш'))
    file = models.FileField(max_length=256, upload_to='%Y/%m/%d', verbose_name=_('путь'))
    user = models.ManyToManyField(to=USER_MODEL, through='UserFile', related_name='files', verbose_name=_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('файл')
        verbose_name_plural = _('файлы')

    def __unicode__(self):
        return '%s' % self.file.name.split('/')[-1]


class Photo(File):
    superclass = models.OneToOneField('File', primary_key=True, db_column='id', parent_link=True)
    load_data = models.DateField(auto_now=True, verbose_name=_('дата загрузки'))
    create_data = models.DateField(verbose_name=_('дата создания'))
    camera_info = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('производитель и модель камеры'))
    file_size = models.PositiveIntegerField(verbose_name=_('размер файла'), blank=True, null=True)

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('фотография')
        verbose_name_plural = _('фотографии')

    def __unicode__(self):
        return '%s' % self.file.name.split('/')[-1]


class UserFile(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('имя'))
    file = models.ForeignKey('File', related_name='userfiles', verbose_name=_('файл'))
    user = models.ForeignKey(USER_MODEL,  related_name='userfiles', verbose_name=_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('пользовательский файл')
        verbose_name_plural = _('пользовательские файлы')

    def __unicode__(self):
        return '%s' % self.title


# Биндим сигналы на удаление и обновление файлов
@receiver(pre_save, sender=Photo)
@receiver(pre_save, sender=File)
def create_hash(instance, *args, **kwargs):
    """
    хэш для проверки уникальности файла
    """
    if instance.hash:
        return
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


@receiver(post_delete, sender=Photo)
@receiver(post_delete, sender=File)
def remove_files(instance, **kwargs):
    """
    Удаление файла с накопителя при удалиние инстанса
    """
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
        if not MAX_USER_FILES_COUNT:
            return instance
        user_files_count = UserFile.objects.filter(user=instance.user).count()
        logger.debug(user_files_count)
        if user_files_count >= MAX_USER_FILES_COUNT:
            logger.debug('so many users files')
            raise PermissionDenied('You have so many files %s!!! You can have %s' % (
                user_files_count, settings.MAX_USER_FILES_COUNT))
        return instance

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
        return instance


@receiver(post_save, sender=Photo)
def get_filesize(instance, *args, **kwargs):
    try:
        if not instance.file_size:
            file = instance.file.file
            file_size = os.stat(instance.file.path).st_size
            instance.file_size = file_size
            instance.save()
            return instance
        return instance
    except OSError, err:
        logger.debug(err)
        return instance
    except AttributeError, err:
        logger.debug(err)
        return instance

@receiver(post_save, sender=Photo)
def get_camera_info(instance, *args, **kwargs):
    try:
        if not instance.camera_info:
            file = instance.file.file
            exif_dict = get_exif_dict(instance.file.path)
            if exif_dict:
                camera_model = exif_dict.get('Model')
                camera_manufacturer = exif_dict.get('Make')
                camera_info = ' '.join([camera_manufacturer, camera_model])
                instance.camera_info = camera_info
                instance.save()
            return instance
        return instance
    except OSError, err:
        logger.debug(err)
        return instance
    except AttributeError, err:
        logger.debug(err)
        raise
        return instance