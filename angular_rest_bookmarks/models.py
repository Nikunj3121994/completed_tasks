# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
try:
    from django.core.exceptions import AppRegistryNotReady
except ImportError:
    AppRegistryNotReady = Exception
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import treebeard.mp_tree
import treebeard.al_tree


logger = logging.getLogger(__name__)

APP_LABEL = 'angular_rest_bookmarks'


try:
    USER_MODEL = get_user_model()
except AppRegistryNotReady, err:
    logger.debug(err)
    USER_MODEL = User
except Exception, err:
    logger.error(err)
    USER_MODEL = User


class Folder_AL(treebeard.al_tree.AL_Node):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    user = models.ForeignKey(
        USER_MODEL, verbose_name='Пользователь', blank=True, null=True, related_name='folders_al')
    # source = models.ForeignKey('source.Source', blank=True, null=True)
    source = models.CharField(
        verbose_name=_('Закладка'), max_length=200, blank=True, null=True)
    parent = models.ForeignKey(
        'self', related_name='children_set', blank=True, null=True, db_index=True)

    node_order_by = ['name']

    def __unicode__(self):
        return 'Раздел: %s' % self.name
