# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .groups import Group


APP_LABEL = 'protokol_auth'


class Role(models.Model):
    """
    Соответствие ролей и LDAP групп.
    """
    name = models.CharField(unique=True, verbose_name='название', max_length=255)
    groups = models.ManyToManyField(Group, blank=True, related_name='roles', verbose_name='группы')

    class Meta:
        app_label = APP_LABEL
        ordering = ['name']

    def __unicode__(self):
        return self.name
