# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings
from .views import (
    GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView, GroupDetailView, GROUP_URL_PK
)


urlpatterns = patterns(
    '',
    url(r'^$', GroupListView.as_view(), name='list'),
    url(r'^(?P<%s>\d+)/$' % GROUP_URL_PK, GroupDetailView.as_view(), name='detail'),
    url(r'^(?P<%s>\d+)/edit/$' % GROUP_URL_PK, GroupUpdateView.as_view(), name='edit'),
)


if settings.PROTOCOL_AUTH_WITH_LDAP is False:
    urlpatterns += patterns(
        '',
        url(r'^add/$', GroupCreateView.as_view(), name='add'),
        url(r'^(?P<%s>\d+)/delete/$' % GROUP_URL_PK, GroupDeleteView.as_view(), name='delete'),
    )
