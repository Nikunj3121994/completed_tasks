# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import logging
from datetime import date

from rest_framework import generics
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.mail import EmailMultiAlternatives

from post_office import mail
from post_office.models import Email

from notifications.models import Notification

from ..serializers import EmailSerializer, NotificationSerializer
from .mixin import AccessMixin
from import_export.admin import ImportMixin

logger = logging.getLogger(__name__)

# todo: переделать в виде viewsets readonly


class NotificationsListAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
