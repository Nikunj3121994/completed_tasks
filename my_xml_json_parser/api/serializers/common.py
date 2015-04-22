# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination

from my_xml_json_parser.models import MyUser, Post, Comment, Like, Photo

logger = logging.getLogger(__name__)


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser


class PostSerializer(serializers.ModelSerializer):
    author = MyUserSerializer()

    # def create(self, validated_data):
    #     pass

    class Meta:
        model = Post


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo