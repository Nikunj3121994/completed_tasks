# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import generics, parsers
from rest_framework.response import Response
from rest_framework import status
from my_files_storage.models import UserFile
from ..serializers import FileSerializer, UserSerializer, UserFileSerializer
from .mixin import AccessMixin

logger = logging.getLogger(__name__)

class UserFileDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'

    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer


class UsersFilesListAPIView(generics.ListAPIView, generics.CreateAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            data = serializer.data
        except PermissionDenied, err:
            data = serializer.data
            data['error'] = str(err)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
