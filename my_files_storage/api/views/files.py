# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.shortcuts import Http404
from django.db import IntegrityError
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework import generics, parsers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from my_files_storage.models import File
from ..serializers import FileSerializer, UserSerializer
from .mixin import AjaxableResponseMixin
from .permissions import AuthorCanEditPermission

logger = logging.getLogger(__name__)

class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # permission_classes = [
    #     AuthorCanEditPermission
    # ]

    # def pre_save(self, obj):
    #     """Force author to the current user on save"""
    #     obj.author = self.request.user
    #     return super(FileDetail, self).pre_save(obj)

class FilesListAPIView(generics.ListAPIView, generics.CreateAPIView, AjaxableResponseMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (parsers.FileUploadParser, parsers.JSONParser)
    # permission_classes = [
    #     AuthorCanEditPermission
    # ]
    #

    def perform_create(self, serializer):

        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            data = serializer.data
        except IntegrityError, err:
            # logger.debug(err)
            pk = str(err).split('_pk_ ')[-1]
            logger.debug(hash)

            file = File.objects.filter(pk = pk).first() #или гетом, если по нраву
            # logger.debug(file)
            serializer = self.get_serializer(file)
            # logger.debug(serializer.data)
            data = serializer.data
            data['error'] = str(err)
            # logger.debug(data)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    # def post(self, request, *args, **kwargs):
    #     logger.debug(request.data)
    #     file_obj = request.data.get('file')
    #     logger.debug(file_obj)
    #     logger.debug(dir(file_obj))
    #     import hashlib
    #     m = hashlib.md5()
    #     while True:
    #         data = file_obj.read(8000)
    #         if not data:
    #             break
    #         m.update(data)
    #
    #     logger.debug(m.hexdigest())
    #     obj = super(FilesListAPIView, self).post(request, *args, **kwargs)
    #     return obj

    #     print request.DATA
    #     print request.POST
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

class FileUserstList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(FileUserstList, self).get_queryset()
        return queryset.filter(files__pk=self.kwargs.get('pk'))