# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination
from post_office.models import Email
from django.contrib.auth.models import User
from rest_framework_hstore.serializers import DictionaryField
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('notification_type', 'title', 'email', 'text', 'title', 'context', 'shop', 'from_user', 'to_user', 'content_type_id', 'object_id')
        exlude = ('id')
