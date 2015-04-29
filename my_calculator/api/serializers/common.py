# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers, pagination


class MyNumberSerializer(serializers.BaseSerializer):
    number = serializers.FloatField()


class MyNumberSerializer(serializers.Serializer):
    number = serializers.FloatField()


class MyLeksemmaSerializer(serializers.Serializer):
    operation = serializers.CharField()
