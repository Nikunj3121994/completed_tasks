# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from protokol.utils import floppyforms as floppy_utils
from protokol.protokol_auth.views import AccessMixin
from .forms import FlatPageForm

URL_PK = 'url_pk'


class FlatPageListView(AccessMixin, ListView):
    allow_administrator = True
    model = FlatPage
    template_name = 'protocol/flat_pages/list.html'
    context_object_name = 'pages'

    def get_queryset(self):
        query = super(FlatPageListView, self).get_queryset()
        return query

class FlatPageCreateView(AccessMixin, CreateView):
    allow_administrator = True
    model = FlatPage
    form_class = floppy_utils.floppify_form(FlatPageForm)
    template_name = 'protocol/flat_pages/add.html'
    context_object_name = 'url'

    def form_valid(self, form):
        # url =
        # form.save()
        # form.save_m2m()
        return super(FlatPageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('protocol:flat_pages:list')



    # def get_queryset(self):
    #     query = super(AuthKeyListView, self).get_queryset()
    #     return query.filter(key_type=KEY_TYPES.AUTH_KEY)

# FlatPageListView



class FlatPageDetailView(AccessMixin, DetailView):
    allow_administrator = True
    pk_url_kwarg = URL_PK
    model = FlatPage
    template_name = 'protocol/flat_pages/detail.html'
    context_object_name = 'url'

    # def get_queryset(self):
    #     query = super(AuthKeyDetailView, self).get_queryset()
    #     return query.filter(key_type=KEY_TYPES.AUTH_KEY)


class FlatPageUpdateView(AccessMixin, UpdateView):
    allow_administrator = True
    pk_url_kwarg = URL_PK
    model = FlatPage
    form_class = floppy_utils.floppify_form(FlatPageForm)
    template_name = 'protocol/flat_pages/edit.html'
    context_object_name = 'url'

    # def form_valid(self, form):
    #     form.save_m2m()
    #     form.save()
    #     return super(FlatPageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('protocol:flat_pages:list')


class FlatPageDeleteView(AccessMixin, DeleteView):
    allow_administrator = True
    pk_url_kwarg = URL_PK
    model = FlatPage
    template_name = 'protocol/flat_pages/delete.html'
    context_object_name = 'url'

    # def get_queryset(self):
    #     query = super(AuthKeyDeleteView, self).get_queryset()
    #     return query.filter(key_type=KEY_TYPES.AUTH_KEY)

    def get_success_url(self):
        return reverse('protocol:flat_pages:list')


# Create your views here.
