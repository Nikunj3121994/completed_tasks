# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.conf import settings


logger = logging.getLogger(__name__)

try:
    import ldap
    from django_auth_ldap.backend import LDAPBackend
except ImportError, err:
    logger.error('ldap impoer error')
    logger.error(err)


def get_ldap_user_uids():

    l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    result = l.search_s(settings.LDAP_SYNC_BASE, ldap.SCOPE_SUBTREE, settings.LDAP_SYNC_FILTER)
    usernames = []
    for i in result:
        usernames.append(i[1]['uid'][0])
    return usernames


def sync_ldap_users(ldap_user_uids):
    backend = LDAPBackend()
    users = {}
    for username in ldap_user_uids:
        users[username] = backend.populate_user(username)
    return users


def syncldap():
    ldap_users = get_ldap_user_uids()
    users = []
    if ldap_users:
        users = sync_ldap_users(ldap_users)
    return users
