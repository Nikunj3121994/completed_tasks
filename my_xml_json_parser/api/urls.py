# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from .views import MyUsersListAPIView, PostsListAPIView, CommentsListAPIView, LikesListAPIView, PhotosListAPIView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns(
    '',
    url(r'^my_users',MyUsersListAPIView.as_view(), name='my_users'),
    url(r'^posts', PostsListAPIView.as_view(), name='posts'),
    url(r'^comments', CommentsListAPIView.as_view(), name='comments'),
    url(r'^likes', LikesListAPIView.as_view(), name='likes'),
    url(r'^photos', PhotosListAPIView.as_view(), name='photos'),
)
