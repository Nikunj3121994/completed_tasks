# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.conf import settings
try:
    from my_auth.views.mixins import AccessMixin
except ImportError:
    AccessMixin = object

class SimpleStaticView(TemplateView, AccessMixin):
    def get_template_names(self):
        return [self.kwargs.get('template_name') + ".html"]

    # def get(self, request, *args, **kwargs):
    #     from django.contrib.auth import authenticate, login
    #     if request.user.is_anonymous():
    #         # Auto-login the User for Demonstration Purposes
    #         user = authenticate()
    #         login(request, user)
    #     return super(SimpleStaticView, self).get(request, *args, **kwargs)