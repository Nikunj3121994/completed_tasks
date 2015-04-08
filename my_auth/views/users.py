# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.http.response import Http404
from django.utils.translation import ugettext as _
from ..forms import UserCreateForm, UserUpdateForm, SetPasswordForm
from .mixins import AccessMixin


USER_URL_PK = 'user_pk'
USER_MODEL = get_user_model()


class UserListView(AccessMixin,  ListView):
    template_name = 'users/list.html'
    model = USER_MODEL
    paginate_by = 50
    context_object_name = 'users'
    allow_administrator = True


class UserDetailView(AccessMixin, DetailView):
    """
    View просмотра пользователя.
    """
    template_name = 'users/detail.html'
    pk_url_kwarg = USER_URL_PK
    model = USER_MODEL
    #allow_administrator = True
    context_object_name = 'user'


class UserCreateView(CreateView):
    """
    View добавления нового пользователя.
    """
    template_name = 'users/add.html'
    model = USER_MODEL
    form_class = UserCreateForm
    #allow_administrator = True

    def get_success_url(self):
        return reverse('auth:login')
        # return reverse('auth:users:detail', kwargs={USER_URL_PK: self.object.pk})


class UserUpdateView(AccessMixin, UpdateView):
    """
    View редактирования пользователя.
    """
    template_name = 'users/edit.html'
    pk_url_kwarg = USER_URL_PK
    model = USER_MODEL
    context_object_name = 'user'
    form_class = UserUpdateForm
    allow_administrator = True

    def get_success_url(self):
        return reverse('auth:users:detail', kwargs={USER_URL_PK: self.object.pk})


class UserDeleteView(AccessMixin, DeleteView):
    """
    View удаления пользователя.
    """
    template_name = 'users/delete.html'
    model = USER_MODEL
    context_object_name = 'user'
    pk_url_kwarg = USER_URL_PK
    allow_administrator = True

    def get_success_url(self):
        return reverse('auth:users:list')


class UserChangePasswordView(AccessMixin, UpdateView):
    """
    View смены пароля пользователя.
    """
    template_name = 'users/change_password.html'
    form_class = SetPasswordForm
    model = USER_MODEL
    context_object_name = 'user'
    pk_url_kwarg = USER_URL_PK
    allow_administrator = True

    def get_form_kwargs(self):
        kwargs = super(UserChangePasswordView, self).get_form_kwargs()
        kwargs.update({'user': kwargs.pop('instance', self.object)})
        return kwargs

    def get_success_url(self):
        return reverse('auth:users:detail', kwargs={USER_URL_PK: self.object.pk})


# TODO: объединить повторяющиеся части
class UserBlockView(AccessMixin, DetailView):
    """
    View блокирования пользователя.
    """
    template_name = 'users/block.html'
    model = USER_MODEL
    context_object_name = 'user'
    pk_url_kwarg = USER_URL_PK
    allow_administrator = True

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('auth:users:detail', kwargs={USER_URL_PK: self.object.pk})


class UserUnblockView(AccessMixin, DetailView):
    """
    View разблокирования пользователя.
    """
    template_name = 'users/unblock.html'
    model = USER_MODEL
    context_object_name = 'user'
    pk_url_kwarg = USER_URL_PK
    allow_administrator = True

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = True
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('auth:users:detail', kwargs={USER_URL_PK: self.object.pk})


class WithUserMixin(object):
    user_pk_url_kwarg = USER_URL_PK

    def get_user(self):
        pk = self.kwargs.get(self.user_pk_url_kwarg, None)
        try:
            user = USER_MODEL.objects.get(pk=pk)
        except USER_MODEL.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': USER_MODEL._meta.verbose_name})
        return user

    def get_context_data(self, **kwargs):
        context = super(WithUserMixin, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context
