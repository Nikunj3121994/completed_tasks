# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.http import Http404
from django.db import IntegrityError
from django.contrib.auth.models import User
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


    # parser_classes = (parsers.FileUploadParser, )
    # parser_classes = (parsers.MultiPartParser, parsers.FileUploadParser, parsers.JSONParser)
    def get_queryset(self):
        type = self.kwargs.get('type')
        try:
            return  self.queryset_dict[type]
        except KeyError,err:
            raise Http404

        # return super(FilesListAPIView, self).get_queryset()

    def get_serializer_class(self):
        type = self.kwargs.get('type')
        try:
            return  self.serializer_class_dict[type]
        except KeyError,err:
            raise Http404
        # return super(FilesListAPIView, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            data = serializer.data
        except IntegrityError, err:
            pk = str(err).split('_pk_ ')[-1]
            # или гетом, если по нраву
            file = File.objects.filter(pk=pk).first()
            serializer = self.get_serializer(file)
            data = serializer.data
            data['error'] = str(err)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):

        # logger.debug(request)
        # logger.debug(request.content_type)
        # # logger.debug(request.stream)
        # logger.debug(request.query_params)
        # logger.debug(request.data)
        # print dir(request)
        # raise Exception
        # print request.FILES
        # print request.QUERY_PARAMS
        # print request._CONTENTTYPE_PARAM
        # print request._METHOD_PARAM
        # print self.request.data
        return super(FilesListAPIView, self).post(request, *args, **kwargs)


class FileUserstList(generics.ListAPIView, AccessMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(FileUserstList, self).get_queryset()
        return queryset.filter(files__pk=self.kwargs.get('pk'))
