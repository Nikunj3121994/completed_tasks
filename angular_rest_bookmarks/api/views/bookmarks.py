# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.shortcuts import Http404
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework import generics
from angular_rest_bookmarks.models import Folder_AL
from ..serializers.bookmarks import BookMarkTreeSerializer
from .mixin import AjaxableResponseMixin
from .permissions import AuthorCanEditPermission

logger = logging.getLogger(__name__)

class BookMarkTreeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Folder_AL.objects.all()
    serializer_class = BookMarkTreeSerializer
    permission_classes = [
        AuthorCanEditPermission
    ]

    def pre_save(self, obj):
        """Force author to the current user on save"""
        if not obj.user:
            obj.user = self.request.user
        return super(BookMarkTreeDetail, self).pre_save(obj)

class BookMarkTreeListAPIView(generics.ListAPIView, generics.CreateAPIView, AjaxableResponseMixin): #todo: добавить необходимость авторизации миксин из протокола
    serializer_class = BookMarkTreeSerializer
    queryset = Folder_AL.objects.all()
    permission_classes = [
        AuthorCanEditPermission
    ]


    def post(self, request, *args, **kwargs):
        logger.debug(request.DATA)
        data = [request.DATA,]
        parent_id = request.DATA.get('parent')
        if not request.DATA['data']['user']: #TODO: убрать этот костыль
            request.DATA['data']['user'] = self.request.user.id
        try:
            parent = Folder_AL.objects.get(id=parent_id)
        except MultipleObjectsReturned:
            pass #todo: сделать колбек с ошибкой
        except ObjectDoesNotExist:
            parent = None
        id = Folder_AL.load_bulk(data, parent)[0]#todo:может возвращать несколько id при работе скопом.
        return self.render_to_json_response({'id': id}, status=200)


    def filter_queryset(self, queryset):
        user = self.request.user
        if user is not AnonymousUser:
            queryset = queryset.filter(user__id=user.id)
        else:
            queryset = queryset.None()
        return queryset.filter(parent = None)
