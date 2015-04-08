# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination

from my_files_storage.models import File, UserFile

logger = logging.getLogger(__name__)

class FileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')


    class Meta:
        model = File

    def get_url(self, obj):
        try:
            return  obj.path.url
        except AttributeError:
            return

    # def get_childrens(self, obj):
    #     childerens = Folder_AL.objects.filter(parent__id=obj.id)
    #     return (self.get_data(child) for child in childerens)
    #
    #
    # def get_tree(self, obj):
    #     return Folder_AL.dump_bulk()
    #
    # def get_self_tree(self, obj):
    #     return Folder_AL.dump_bulk(parent=obj)
    #
    # def get_data(self, obj):
    #     data = dict((i.name, obj.__dict__[i.column]) for i in obj._meta.local_fields)
    #     return data
