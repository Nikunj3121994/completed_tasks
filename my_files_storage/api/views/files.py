# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.http import Http404
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework import generics, parsers
from rest_framework.response import Response
from rest_framework import status
from my_files_storage.models import File, Photo
from ..serializers import FileSerializer, PhotoSerializer, UserSerializer
from .mixin import AccessMixin

logger = logging.getLogger(__name__)


class FileDetail(generics.RetrieveUpdateDestroyAPIView, AccessMixin):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FilesListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin):
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
            return  self.queryset_dict[type]
        except KeyError,err:
            raise Http404

    def get_serializer_class(self):
        type = self.kwargs.get('type')
        try:
            return  self.serializer_class_dict[type]
        except KeyError,err:
            raise Http404
        # return super(FilesListAPIView, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise PermissionDenied(serializer.errors)
        self.perform_create(serializer)
        data = serializer.data
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return super(FilesListAPIView, self).post(request, *args, **kwargs)


class FileUserstList(generics.ListAPIView, AccessMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(FileUserstList, self).get_queryset()
        return queryset.filter(files__pk=self.kwargs.get('pk'))
