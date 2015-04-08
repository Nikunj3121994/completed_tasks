# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings


APP_LABEL = 'protokol_auth'
USER_MODEL = settings.AUTH_USER_MODEL


class Group(models.Model):
    """
    Группа пользователей.
    """
    name = models.CharField(unique=True, verbose_name='название', max_length=255)
    users = models.ManyToManyField(USER_MODEL, blank=True, related_name='groups', verbose_name='пользователи')

    class Meta:
        app_label = APP_LABEL
        ordering = ['name']
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __unicode__(self):
        return self.name
