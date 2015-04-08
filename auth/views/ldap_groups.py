# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .mixins import AccessMixin
from django_ldap_groups.models import LDAPGroup


GROUP_URL_PK = 'group_pk'


class LDAPGroupListView(AccessMixin, ListView):
    template_name = 'ldap_groups/list.html'
    model = LDAPGroup
    paginate_by = 50
    context_object_name = 'ldap_groups'
    allow_administrator = True


class LDAPGroupDetailView(AccessMixin, DetailView):
    template_name = 'ldap_groups/detail.html'
    model = LDAPGroup
    context_object_name = 'ldap_group'
    allow_administrator = True
    pk_url_kwarg = GROUP_URL_PK
