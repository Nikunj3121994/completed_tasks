# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.shortcuts import Http404
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework import generics, parsers
from django.contrib.auth.models import User
from my_files_storage.models import UserFile
from ..serializers import FileSerializer, UserSerializer, UserFileSerializer
from .mixin import AjaxableResponseMixin
from .permissions import AuthorCanEditPermission

logger = logging.getLogger(__name__)

class UserFileDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'

    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer
    # permission_classes = [
    #     AuthorCanEditPermission
    # ]

    # def pre_save(self, obj):
    #     """Force author to the current user on save"""
    #     obj.author = self.request.user
    #     return super(FileDetail, self).pre_save(obj)

class UsersFilesListAPIView(generics.ListAPIView, generics.CreateAPIView, AjaxableResponseMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer

    # parser_classes = (parsers.FileUploadParser, parsers.JSONParser)
    # permission_classes = [
    #     AuthorCanEditPermission
    # ]
    #

    # def post(self, request, *args, **kwargs):
    #     print request
    #     # logger.debug(request.DATA)
    #     # logger.debug(request.POST)
    #     # logger.debug(dir(request))
    #     logger.debug(request.FILES)
    #     logger.debug(request.data)
    #     return request
    #     data = [request.DATA,]
    #     parent_id = request.DATA.get('parent')
    #     try:
    #         parent = Folder_AL.objects.get(id=parent_id)
    #     except MultipleObjectsReturned:
    #         pass #todo: сделать колбек с ошибкой
    #     except ObjectDoesNotExist:
    #         parent = None
    #     id = Folder_AL.load_bulk(data, parent)[0]#todo:может возвращать несколько id при работе скопом.
    #     return self.render_to_json_response({'id': id}, status=200)
    #
    #
    # def filter_queryset(self, queryset):
    #     user = self.request.user
    #     if user is not AnonymousUser:
    #         queryset = queryset.filter(user__id=user.id)
    #     else:
    #         queryset = queryset.None()
    #     return queryset.filter(parent = None)

# class FileUserstList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         queryset = super(FileUserstList, self).get_queryset()
#         return queryset.filter(files__pk=self.kwargs.get('pk'))
#
# class UserFilestList(generics.ListAPIView):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#
#     def get_queryset(self):
#         queryset = super(UserFilestList, self).get_queryset()
#         return queryset.filter(user__id=self.kwargs.get('pk'))