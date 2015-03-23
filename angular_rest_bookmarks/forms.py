# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from treebeard.forms import MoveNodeForm
from floppyforms import forms


# try:
#     from django_summernote.widgets import SummernoteInplaceWidget as Widget
# except ImportError:
#     from django.forms.widgets import Textarea as Widget
# #from floppyforms.forms import forms
# from django.contrib.flatpages.models import FlatPage
#
#
#
#
# # class MoveNodeForm()
#
# class FlatPageForm(forms.ModelForm):
#     class Meta:
#         model = FlatPage
#         fields = ['title', 'url', 'content', 'template_name', 'sites']
#         if 'django_summernote' in settings.INSTALLED_APPS:
#             widgets = {
#                 'content': Widget(),
#             }
