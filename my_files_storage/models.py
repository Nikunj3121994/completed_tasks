# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django import forms
try:
    from django.core.exceptions import AppRegistryNotReady
except ImportError:
    AppRegistryNotReady = Exception
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from utils import bind_delete_update_file


logger = logging.getLogger(__name__)

APP_LABEL = 'my_files_storage'


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
    hash = models.CharField(max_length=255, unique=True, blank=True, verbose_name=_('хэш'))
    file = models.FileField(max_length=256, upload_to="%Y/%m/%d", verbose_name=_('путь'))
    user = models.ManyToManyField(to=USER_MODEL, through='UserFile', related_name='files', verbose_name =_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('файл')
        verbose_name_plural = _('файлы')

    def __unicode__(self):
        return '%s' % self.file.name.split('/')[-1]


class UserFile(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('имя'))
    file = models.ForeignKey(File, related_name='userfiles', verbose_name=_('файл'))
    user = models.ForeignKey(User,  related_name='userfiles', verbose_name=_('пользователь'))

    class Meta:
        app_label = APP_LABEL
        verbose_name = _('пользовательский файл')
        verbose_name_plural = _('пользовательские файлы')

    def __unicode__(self):
        return '%s' % self.title


#Биндим сигналы на удаление и обновление файлов
bind_delete_update_file([File,])


@receiver(pre_save, sender=File)
def create_hash(instance, *args, **kwargs):
    # logger.debug(instance)
    # logger.debug(args)
    # logger.debug(kwargs)
    # logger.debug(instance.file.url)
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
    older_file = File.objects.filter(hash = instance.hash)
    if older_file:
        raise IntegrityError('object already: _pk_ %s'%older_file.first().pk)
    return instance


@receiver(pre_save, sender=File)
def change_count_link(instance, *args, **kwargs):
    logger.debug(instance)
    logger.debug(args)
    logger.debug(kwargs)
    # logger.debug(dir(kwargs['signal']))
    # logger.debug(kwargs['signal'].__dict__)
    # logger.debug(kwargs['signal'].__class__)
    if not instance.pk:
        return
    elif instance.user.count() < 1:
       # logger.debug(instance.userfiles.count())
        logger.debug(instance.user.count())
        logger.debug('need to delete files')
        #instance.delete()
    else:
       # logger.debug(instance.userfiles.count())
        logger.debug('%s link on file'%instance.user.count())

    return

@receiver(m2m_changed, sender=File)
def change_count_link(instance, *args, **kwargs):
    logger.debug(instance)
    logger.debug(args)
    logger.debug(kwargs)
    # logger.debug(dir(kwargs['signal']))
    # logger.debug(kwargs['signal'].__dict__)
    # logger.debug(kwargs['signal'].__class__)
    if not instance.pk:
        return
    elif instance.user.count() < 1:
       # logger.debug(instance.userfiles.count())
        logger.debug(instance.user.count())
        logger.debug('need to delete files')
        #instance.delete()
    else:
       # logger.debug(instance.userfiles.count())
        logger.debug('%s link on file'%instance.user.count())

    return

@receiver(post_save, sender=File)
def change_count_link(instance, *args, **kwargs):
    logger.debug(instance)
    logger.debug(args)
    logger.debug(kwargs)
    # logger.debug(dir(kwargs['signal']))
    # logger.debug(kwargs['signal'].__dict__)
    # logger.debug(kwargs['signal'].__class__)
    if not instance.pk:
        return
    elif instance.user.count() < 1:
       # logger.debug(instance.userfiles.count())
        logger.debug(instance.user.count())
        logger.debug('need to delete files')
        #instance.delete()
    else:
       # logger.debug(instance.userfiles.count())
        logger.debug('%s link on file'%instance.user.count())

    return

@receiver(pre_save, sender=User)
@receiver(m2m_changed, sender=File)
def user_file_limit(instance, *args, **kwargs):
    logger.debug(instance)
    logger.debug(args)
    logger.debug(kwargs)
    if not instance.pk:
        return
    elif instance.files.count() > 100:
        logger.debug('so many users files')
        # instance.delete()
    else:
        logger.debug('%s link on file'%instance.files.count())

    return

@receiver(post_save, sender=User)
@receiver(m2m_changed, sender=File)
def user_file_limit(instance, *args, **kwargs):
    logger.debug(instance)
    logger.debug(args)
    logger.debug(kwargs)
    if not instance.pk:
        return
    elif instance.files.count() > 100:
        logger.debug('so many users files')
        # instance.delete()
    else:
        logger.debug('%s link on file'%instance.files.count())

    return

@receiver(pre_delete, sender=UserFile)
@receiver(pre_save, sender=UserFile)
def change_count_link(instance, *args, **kwargs):
    logger.debug(instance)
    logger.debug(args)
    logger.debug(kwargs)
    logger.debug(UserFile.objects.filter(user=instance.user).count())
    logger.debug(UserFile.objects.filter(file=instance.file).count())
    user_files_count = UserFile.objects.filter(user=instance.user).count()
    files_link_count = UserFile.objects.filter(file=instance.file).count()
    if user_files_count >= 99:
        logger.debug('so many users files')
        raise forms.ValidationError('so many files')
    if files_link_count <= 1:
        logger.debug('need to delete files')
    return