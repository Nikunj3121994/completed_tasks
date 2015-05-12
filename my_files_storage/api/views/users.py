# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from rest_framework import generics
from django.contrib.auth.models import User
from my_files_storage.models import File, Photo, UserFile
from ..serializers import FileSerializer, PhotoSerializer, UserSerializer, UserFileSerializer
from .mixin import AccessMixin


class UserDetail(generics.RetrieveUpdateDestroyAPIView, AccessMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# todo: переделать через permissions
class UsersListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFilesList(generics.ListAPIView, generics.CreateAPIView, AccessMixin):
    queryset_dict = {
        'files':File.objects.all(),
        'photos':Photo.objects.all(),
    }
    serializer_class_dict = {
        'files':FileSerializer,
        'photos':PhotoSerializer,
    }

    def get_queryset(self):
        type = self.kwargs.get('type')
        try:
            return  self.queryset_dict[type].filter(user__id=self.kwargs.get('pk'))
        except KeyError,err:
            raise Http404

    def get_serializer_class(self):
        type = self.kwargs.get('type')
        try:
            return  self.serializer_class_dict[type]
        except KeyError,err:
            raise Http404
