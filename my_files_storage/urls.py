# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings



urlpatterns = patterns('',
    url(r'^api/', include('my_files_storage.api.urls', namespace='api')),
)

