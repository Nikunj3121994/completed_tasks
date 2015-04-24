# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import SimpleStaticView, AuthTemplateView


urlpatterns = patterns('',
    url(r'^api/', include('angular_rest_bookmarks.api.urls', namespace='api')),
    url(r'^bookmarks_example$', AuthTemplateView.as_view(template_name='bookmark_example.html'), name='example')
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^(?P<template_name>\w+)$', SimpleStaticView.as_view(), name='example'),
                            )
