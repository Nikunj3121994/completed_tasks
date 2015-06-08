
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from post_office import mail
from post_office.models import EmailTemplate
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


def sending_mail(*args, **kwargs):
    mail.send(
        'chaotism@mail.ru', # List of email addresses also accepted
        'chaotism@mail.ru',
        subject='My email',
        message='Hi there!',
        html_message='Hi <strong>there</strong>!',
    )

    mail.send(
        ['recipient1@example.com'],
        'from@example.com',
        subject='Welcome!',
        message='Welcome home, {{ name }}!',
        html_message='Welcome home, <b>{{ name }}</b>!',
        headers={'Reply-to': 'reply@example.com'},
        scheduled_time=date(2014, 1, 1),
        context={'name': 'Alice'},
    )

    EmailTemplate.objects.create(
        name='morning_greeting',
        subject='Morning, {{ name|capfirst }}',
        content='Hi {{ name }}, how are you feeling today?',
        html_content='Hi <strong>{{ name }}</strong>, how are you feeling today?',
    )

    mail.send(
        ['recipient@example.com'],
        'from@example.com',
        template='morning_greeting',
        context={'name': 'alice'},
    )

    # This will create an email with the following content:
    subject = 'Morning, Alice',
    content = 'Hi alice, how are you feeling today?'
    content = 'Hi <strong>alice</strong>, how are you feeling today?'# Create your views here.
