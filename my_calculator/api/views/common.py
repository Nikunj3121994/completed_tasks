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

class MyNumberListAPIView(generics.ListAPIView, AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = [{'number':number[1]} for number in enumerate(xrange(0, 10000))]
    serializer_class = MyNumberSerializer
    paginate_by = 100

class MyLexemmeListAPIView(generics.ListAPIView,  AccessMixin): #todo: добавить необходимость авторизации миксин из протокола
    queryset = [{'operation':r'+'}, {'operation':r'/'}, {'operation':r'*'}, {'operation':r'-'}]
    serializer_class = MyLeksemmaSerializer
    paginate_by = 100


class MyResultDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return Response(eval(request.path.split('/api/')[-1]))
        except (ZeroDivisionError, OverflowError, FloatingPointError),err:
            return Response(str(err))
        except Exception,err:
            logger.error(err)
            return Response(str(err))