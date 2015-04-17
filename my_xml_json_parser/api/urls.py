# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from .views import MyUsersListAPIView, PostsListAPIView, CommentsListAPIView, LikesListAPIView, PhotosListAPIView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns(
    '',
    url(r'^my_users',MyUsersListAPIView.as_view(), namespace='my_users'),
    url(r'^posts', PostsListAPIView.as_view(), namespace='posts'),
    url(r'^comments', CommentsListAPIView.as_view(), namespace='comments'),
    url(r'^likes', LikesListAPIView.as_view(), namespace='likes'),
    url(r'^photos', PhotosListAPIView.as_view(), namespace='photos'),
)
