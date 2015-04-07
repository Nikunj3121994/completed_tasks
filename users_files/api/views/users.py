# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import Http404
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework import generics
from users_files.models import User_file, File
from ..serializers import FileSerializer, UserSerializer
from .mixin import AjaxableResponseMixin
from .permissions import AuthorCanEditPermission




class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User_file.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [
    #     AuthorCanEditPermission
    # ]
    #
    # def pre_save(self, obj):
    #     """Force author to the current user on save"""
    #     obj.author = self.request.user
    #     return super(BookMarkTreeALDetail, self).pre_save(obj)

class UsersAPIView(generics.ListAPIView, generics.CreateAPIView, AjaxableResponseMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = User_file.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [
    #     AuthorCanEditPermission
    # ]
    #
    #
    # def post(self, request, *args, **kwargs):
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

class UserFilestList(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        queryset = super(UserFilestList, self).get_queryset()
        return queryset.filter(users__id=self.kwargs.get('pk'))