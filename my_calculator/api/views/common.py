# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import generics
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from ..serializers import MyLeksemmaSerializer, MyNumberSerializer
from .mixin import AccessMixin


logger = logging.getLogger(__name__)

#todo: переделать в виде viewsets readonly

class MyNumberListAPIView(generics.ListAPIView, AccessMixin):
    queryset = [{'number':number[1]} for number in enumerate(xrange(0, 10))]
    serializer_class = MyNumberSerializer
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class MyLexemmeListAPIView(generics.ListAPIView,  AccessMixin):
    queryset = [{'operation':r'.'}, {'operation':r'+'}, {'operation':r'-'}, {'operation':r'*'}, {'operation':r'/'},]
    serializer_class = MyLeksemmaSerializer
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class MyResultDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return Response(eval(kwargs.get('operation')))
        except (ZeroDivisionError, OverflowError, FloatingPointError), err:
            return Response(str(err))
        except Exception,err:
            logger.error(str(err))
            return Response(str(err))


class WrongOperationView(generics.RetrieveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    error = 'corrupted operation'

    def get(self, request, *args, **kwargs):

        return Response(self.error)