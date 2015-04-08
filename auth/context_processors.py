# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings


def ldap_auth(request):
    """
    Возвращает значение настройки приложения 'PROTOCOL_AUTH_WITH_LDAP' или False
    """
    return {
        'AUTH_WITH_LDAP': getattr(settings, 'PROTOCOL_AUTH_WITH_LDAP', False),
    }


def remote_user(request):
    """
    Возвращает 'REMOTE_USER' из запроса.
    """
    return {
        'REMOTE_USER': request.META.get('REMOTE_USER'),
    }
