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

APP_LABEL = 'my_xml_json_parser'


try:
    USER_MODEL = get_user_model()
except AppRegistryNotReady,err:
    logger.debug(err)
    USER_MODEL = User
except Exception,err:
    logger.error(err)
    USER_MODEL = User


logger = logging.getLogger(__name__)


class Source(models.Model):
    raw_file = models.FileField(upload_to="%Y/%m/%d", verbose_name='resource_file')
    json_file = models.FileField(upload_to="%Y/%m/%d", verbose_name='json_source')

    def __unicode__(self):
        return '%s' % self.raw_file.name.split('/')[-1]

class MyUser(models.Model):
    user = models.OneToOneField(USER_MODEL, related_name='my_user')
    followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)
    nickname = models.CharField(max_length=25)

    def __unicode__(self):
        return '%s' % self.nickname


class Post(models.Model):
    author = models.ForeignKey('MyUser', related_name='posts', blank=True, null=True,)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    #like = models.OneToOneField('Like', related_name='posts')

    def __unicode__(self):
        return '%s' % self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', blank=True, null=True,)
    author = models.ForeignKey('MyUser', related_name='comments')
    #like = models.OneToOneField('Like', related_name='comments')
    text = models.CharField(max_length=400)

    def __unicode__(self):
        return '%s' % self.text


class Photo(models.Model):
    post = models.ForeignKey('Post', related_name='photos', blank=True, null=True,)
    image = models.ImageField(upload_to="%Y/%m/%d")
    #like = models.OneToOneField('Like', related_name='photos')

    def __unicode__(self):
        return '%s' % self.image.name.split('/')[-1]


class Like(models.Model):
    post = models.ForeignKey('Post', related_name='likes', blank=True, null=True, )
    comment = models.ForeignKey('Comment', related_name='likes', blank=True, null=True,)
    photo = models.ForeignKey('Photo', related_name='likes', blank=True, null=True,)
    author = models.ForeignKey('MyUser', related_name='likes', blank=True, null=True,)
    count = models.SmallIntegerField()

    class Meta:
        pass

    def __unicode__(self):
        return '%s like %s %s match' % (self.post, self.author, self.count)