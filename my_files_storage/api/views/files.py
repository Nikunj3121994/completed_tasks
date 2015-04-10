# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import generics, parsers
from rest_framework.response import Response
from rest_framework import status
from my_files_storage.models import File
from ..serializers import FileSerializer, UserSerializer
from .mixin import AccessMixin

logger = logging.getLogger(__name__)


class FileDetail(generics.RetrieveUpdateDestroyAPIView, AccessMixin):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FilesListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (parsers.FileUploadParser, parsers.JSONParser)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            data = serializer.data
        except IntegrityError, err:
            pk = str(err).split('_pk_ ')[-1]
            file = File.objects.filter(pk = pk).first() #или гетом, если по нраву
            serializer = self.get_serializer(file)
            data = serializer.data
            data['error'] = str(err)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class FileUserstList(generics.ListAPIView, AccessMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(FileUserstList, self).get_queryset()
        return queryset.filter(files__pk=self.kwargs.get('pk'))