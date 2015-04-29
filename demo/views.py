# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.conf import settings
try:
    from my_auth.views.mixins import AccessMixin
except ImportError:
    AccessMixin = object


class SimpleStaticView(AccessMixin, TemplateView):

    def get_template_names(self):
        return [self.kwargs.get('template_name') + '.html']


class AuthTemplateView(AccessMixin, TemplateView):
    pass
