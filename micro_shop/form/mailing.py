# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.admin import widgets
from ..models import Mailinglist
from ..choices import SOURCE_FILE_EXTENSIONS

logger = logging.getLogger(__name__)


class MailingImportForm(forms.ModelForm):

    class Meta:
        model = Mailinglist
        exclude = ('shop', 'user')
