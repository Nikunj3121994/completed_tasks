# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.contrib.auth.models import User
from my_files_storage.models import  File, UserFile
from ..serializers import FileSerializer, UserSerializer, UserFileSerializer
from .mixin import AccessMixin




class UserDetail(generics.RetrieveUpdateDestroyAPIView, AccessMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFilestList(generics.ListAPIView, generics.CreateAPIView, AccessMixin):
    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer

    def get_queryset(self):
        queryset = super(UserFilestList, self).get_queryset()
        return queryset.filter(user__id=self.kwargs.get('pk'))