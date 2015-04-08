# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from protokol.utils import floppyforms as floppy_utils
from ..models import Group
from ..forms import GroupBaseForm, GroupLDAPForm
from .mixins import AccessMixin, SyncLDAPViewMixin


GROUP_URL_PK = 'group_pk'


class GroupListView(AccessMixin, SyncLDAPViewMixin, ListView):
    template_name = 'groups/list.html'
    model = Group
    paginate_by = 50
    context_object_name = 'groups'
    allow_administrator = True


class GroupDetailView(AccessMixin, SyncLDAPViewMixin, DetailView):
    """
    View просмотра пользователя.
    """
    template_name = 'groups/detail.html'
    pk_url_kwarg = GROUP_URL_PK
    model = Group
    allow_administrator = True
    context_object_name = 'group'


class GroupCreateView(AccessMixin, CreateView):
    """
    View добавления нового пользователя.
    """
    template_name = 'groups/add.html'
    model = Group
    form_class = floppy_utils.floppify_form(GroupBaseForm)
    allow_administrator = True

    def get_success_url(self):
        return reverse('protocol:groups:detail', kwargs={GROUP_URL_PK: self.object.pk})


class GroupUpdateView(AccessMixin, UpdateView):
    """
    View редактирования пользователя.
    """
    template_name = 'groups/edit.html'
    pk_url_kwarg = GROUP_URL_PK
    model = Group
    context_object_name = 'group'
    form_class = floppy_utils.floppify_form(GroupLDAPForm if settings.PROTOCOL_AUTH_WITH_LDAP else GroupBaseForm)
    allow_administrator = True

    def get_success_url(self):
        return reverse('protocol:groups:list')
        #return reverse('protocol:groups:detail', kwargs={GROUP_URL_PK: self.object.pk})


class GroupDeleteView(AccessMixin, DeleteView):
    """
    View группы.
    """
    template_name = 'groups/delete.html'
    model = Group
    context_object_name = 'group'
    pk_url_kwarg = GROUP_URL_PK
    allow_administrator = True

    def get_success_url(self):
        return reverse('protocol:groups:list')
