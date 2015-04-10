# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import generics, parsers
from django.contrib.auth.models import User
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

