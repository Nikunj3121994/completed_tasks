# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import SimpleStaticView, AuthTemplateView, ImportMailingView, MailingStatusView


urlpatterns = patterns('',
                       url(r'^api/',
                           include('notifications.api.urls', namespace='api')),
                       url(r'^import_mailing$', ImportMailingView.as_view(), name='import_mailing'),
                       url(r'^mailing_status/(?P<pk>\d+)$', MailingStatusView.as_view(), name='mailing_status'),
                       # url(r'^users_photos$', AuthTemplateView.as_view(
                       #     template_name='users_photos.html',), name='users_photos')
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^(?P<template_name>\w+)$',
                                SimpleStaticView.as_view(), name='example'),
                            )
