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

#from ..serializers import MyLeksemmaSerializer, MyNumberSerializer
from ..serializers import EmailSerializer
from .mixin import AccessMixin


logger = logging.getLogger(__name__)

# todo: переделать в виде viewsets readonly


# class MyNumberListAPIView(generics.ListAPIView, AccessMixin):
#     queryset = [{'number': number[1]} for number in enumerate(xrange(0, 10))]
#     serializer_class = MyNumberSerializer
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class MyLexemmeListAPIView(generics.ListAPIView,  AccessMixin):
#     queryset = [{'operation': r'.'}, {'operation': r'+'},
#                 {'operation': r'-'}, {'operation': r'*'}, {'operation': r'/'}, ]
#     serializer_class = MyLeksemmaSerializer
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class MyResultDetailView(generics.RetrieveAPIView):
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, *args, **kwargs):
#         try:
#             return Response(eval(kwargs.get('operation')))
#         except (ZeroDivisionError, OverflowError, FloatingPointError), err:
#             return Response(str(err))
#         except Exception, err:
#             logger.error(str(err))
#             return Response(str(err))
#
#
# class WrongOperationView(generics.RetrieveAPIView):
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#     error = 'corrupted operation'
#
#     def get(self, request, *args, **kwargs):
#         return Response(self.error)


class SendEmailDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return Response(self.send_email_with_postmaster())
        except (ZeroDivisionError, OverflowError, FloatingPointError), err:
            return Response(str(err))
        except Exception, err:
            logger.error(str(err))
            return Response(str(err))

    def send_email(self):
        #TODO: Заменить заглушку
        msg = EmailMultiAlternatives("Subject", "text body","chaotism@rambler.ru", ["chaotism@mail.ru"])
        msg.attach_alternative("<html>html body</html>", "text/html")
        msg.send()
        response = msg.mandrill_response[0]
        return response

        mandrill_id = response['_id']

    def send_email_with_postmaster(self):
        email = mail.send(
            ['recipient1@example.com'],
            'from@example.com',
            subject='Welcome!',
            message='Welcome home, {{ name }}!',
            html_message='Welcome home, <b>{{ name }}</b>!',
            headers={'Reply-to': 'reply@example.com'},
            scheduled_time=date(2014, 1, 1),
            context={'name': 'Alice'},
        )
        # response = mail.mandrill_response[0]
        return email.status


class EmailsListAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
