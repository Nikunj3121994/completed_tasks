# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings



urlpatterns = patterns('',
    url(r'^api/', include('users_files.api.urls', namespace='api')),
)

