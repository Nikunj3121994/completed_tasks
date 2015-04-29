# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers, pagination
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # tree = serializers.SerializerMethodField('get_tree')
    # self__tree = serializers.SerializerMethodField('get_self_tree')
    # children = serializers.SerializerMethodField('get_childrens')
    # data = serializers.SerializerMethodField('get_data')

    class Meta:
        model = User
