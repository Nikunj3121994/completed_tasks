# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from .views import UserListAPIView, UserDetail, UserFilestList, FilesListAPIView, FilesDetail, FileUserstList

from rest_framework.urlpatterns import format_suffix_patterns

users_urls = patterns(
    '',
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^/(?P<pk>\d+)$', UserDetail.as_view(), name='detail'),
    url(r'^/(?P<pk>\d+)/files$', UserFilestList.as_view(), name='userfile-list'),

)

files_urls = patterns(
    '',
    url(r'^$', FilesListAPIView.as_view(), name='list'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', FilesDetail.as_view(), name='detail'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/users$', FileUserstList.as_view(), name='fileuser-list'),
)

urlpatterns = patterns(
    '',
    url(r'^users', include(users_urls , namespace='users')),
    url(r'^files', include(files_urls , namespace='files')),
    # url(r'^$', BookMarkTreeMPAPIView.as_view(), name='list'),
    # url(r'^$', BookMarkTreeALAPIView.as_view(), name='list'),
    # url(r'^/(?P<pk>\d+)$',BookMarkTreeALDetail.as_view(), name='detail'),

)
