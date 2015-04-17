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
except AppRegistryNotReady,err:
    logger.debug(err)
    USER_MODEL = User
except Exception,err:
    logger.error(err)
    USER_MODEL = User


logger = logging.getLogger(__name__)



class MyUser(models.Model):
    followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)
    username = models.CharField(max_length=255)

class Post(models.Model):
    author = models.ForeignKey(MyUser, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)

class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos')
    image = models.ImageField(upload_to="%Y/%m/%d")

class Likes(models.Model):
    post = models.ForeignKey(Post, related_name='likes')
    author = models.ForeignKey(MyUser, related_name='likes')
    count = models.SmallIntegerField()

class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(MyUser, related_name='comments')