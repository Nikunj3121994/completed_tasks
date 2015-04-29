# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import SimpleStaticView, AuthTemplateView


urlpatterns = patterns('',
                       url(r'^api/',
                           include('my_files_storage.api.urls', namespace='api')),
                       url(r'^users_files$', AuthTemplateView.as_view(
                           template_name='users_files.html',), name='users_files')
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^(?P<template_name>\w+)$',
                                SimpleStaticView.as_view(), name='example'),
                            )
