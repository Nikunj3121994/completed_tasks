# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination

from my_xml_json_parser.models import MyUser, Post, Comments, Likes, Photo

logger = logging.getLogger(__name__)

class FileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_my_file_url')


    class Meta:
        model = File

    def get_my_file_url(self, obj):
        try:
            return  obj.file.url
        except AttributeError:
            return


