# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.contrib.auth.models import User
from my_xml_json_parser.models import MyUser, Post, Comment, Like, Photo
from ..serializers import MyUserSerializer, PostSerializer, CommentSerializer, LikeSerializer, PhotoSerializer
from .mixin import AccessMixin


class MyUsersListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class PostsListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentsListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikesListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = Like.objects.all()
    serializer_class =  LikeSerializer


class PhotosListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = Photo.objects.all()
    serializer_class =  PhotoSerializer