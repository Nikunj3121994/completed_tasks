# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination
from django.core.exceptions import ObjectDoesNotExist

from my_files_storage.models import UserFile

logger = logging.getLogger(__name__)

class UserFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_my_file_url')


    class Meta:
        model = UserFile

    def get_my_file_url(self, obj):
        try:
            return  obj.file.file.url
        except (AttributeError, ObjectDoesNotExist):
            return


