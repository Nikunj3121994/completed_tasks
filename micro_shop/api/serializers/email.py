# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination
from post_office.models import Email
from django.contrib.auth.models import User
from rest_framework_hstore.serializers import DictionaryField

# class MyNumberSerializer(serializers.BaseSerializer):
#     number = serializers.FloatField()
#
#
# class MyNumberSerializer(serializers.Serializer):
#     number = serializers.FloatField()
#
#
# class MyLeksemmaSerializer(serializers.Serializer):
#     operation = serializers.CharField()


class EmailSerializer(serializers.ModelSerializer):
    context = DictionaryField(blank=False)
    from_email = serializers.EmailField(max_length=255, )
    to = serializers.EmailField(max_length=255, allow_blank=True )
    cc = serializers.EmailField(max_length=255, allow_blank=True)
    bcc = serializers.EmailField(max_length=255, allow_blank=True)
    # subject = serializers.CharField(max_length=255)
    # message = serializers.CharField()
    # html_message = serializers.CharField()
    """
    # Emails with 'queued' status will get processed by ``send_queued`` command.
    # Status field will then be set to ``failed`` or ``sent`` depending on
    # whether it's successfully delivered.
    # """
    # status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, db_index=True,
    #                                           blank=True, null=True)
    # priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES,
    #                                             blank=True, null=True)
    # created = models.DateTimeField(auto_now_add=True, db_index=True)
    # last_updated = models.DateTimeField(db_index=True, auto_now=True)
    # scheduled_time = models.DateTimeField(blank=True, null=True, db_index=True)
    # headers = JSONField(blank=True, null=True)
    # template = models.ForeignKey('post_office.EmailTemplate', blank=True, null=True)
    # context = context_field_class(blank=True, null=True)

    class Meta:
        model = Email
        fields = ('from_email', 'to', 'cc', 'bcc', 'subject', 'message', 'html_message', 'priority', 'template', 'context')