# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import loader, Context
import json
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.utils.translation import to_locale, get_language, ugettext as _
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe



class MultiFileInput(widgets.AdminFileWidget):

    def render(self, name, value, attrs=None):
        attrs['multiple'] = 'true'
        output = super(MultiFileInput, self).render(name, value, attrs=attrs)
        return mark_safe(output)


