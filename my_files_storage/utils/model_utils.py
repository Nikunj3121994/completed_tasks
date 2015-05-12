# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import importlib

import os
import logging
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.db.models.loading import cache
from django.core.files.storage import get_storage_class

logger = logging.getLogger(__name__)


def convert_filesize(field):
    _extend = ('Б', 'Кб', 'Мб', 'Гб', 'Тб', 'Пб', 'Эб', 'Зб', 'Йб')
    try:
        size = int(field)
        logger.debug('now size %f' % size)
        for i in xrange(len(_extend) - 1):
            size, modulo = divmod(size, 1024)
            if size < 1024:
                size += modulo / 1024.0
                size = ('%.2f' % size).rstrip('0').rstrip('.')
                return '%s %s' % (size, _extend[i + 1])
    except IndexError:
        return '%s байт' % field
    except (ValueError, TypeError), err:
        logger.error('Value or type error with field convert')
        logger.error(field)
        logger.error(err)
        return None
    except UnicodeEncodeError, err:
        logger.error('Unicode error with field convert')
        logger.error(field)
        logger.error(err)
        return field


def find_models_with_filefield():
    for app in cache.get_apps():
        model_list = cache.get_models(app)
        for model in model_list:
            for field in model._meta.fields:
                if isinstance(field, models.FileField):
                    pre_save.connect(remove_old_files, sender=model)
                    post_delete.connect(remove_files, sender=model)
                    break


def bind_delete_update_file(models):
    for model in models:
        pre_save.connect(remove_old_files, sender=model)
        post_delete.connect(remove_files, sender=model)


def remove_old_files(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = instance.__class__.objects.get(pk=instance.pk)
    except instance.DoesNotExist:
        return

    for field in instance._meta.fields:
        if not isinstance(field, models.FileField):
            continue
        old_file = getattr(old_instance, field.name)
        new_file = getattr(instance, field.name)
        storage = old_file.storage
        if old_file and old_file != new_file and storage and storage.exists(old_file.name):
            try:
                storage.delete(old_file.name)
            except Exception:
                logger.exception(
                    "Unexpected exception while attempting to delete old file '%s'" % old_file.name)


def remove_files(sender, instance, **kwargs):
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
