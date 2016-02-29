# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers, pagination
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
