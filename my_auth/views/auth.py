# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from ..forms import AuthenticationForm


class LoginBaseView(FormView):

    """Основа для страницы входа пользователя."""
    redirect_field_name = REDIRECT_FIELD_NAME
    form_class = AuthenticationForm
    default_redirect_url = settings.LOGIN_REDIRECT_URL

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(self.default_redirect_url)
        return redirect_to

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginBaseView, self).form_valid(form)

    def form_invalid(self, form):
        # print form.errors
        return super(LoginBaseView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginBaseView, self).get_context_data(**kwargs)
        context['redirect_data'] = self.request.REQUEST.get(
            self.redirect_field_name, '')
        context['redirect_field_name'] = self.redirect_field_name
        return context


class LogoutBaseView(TemplateView):

    """Основа для страницы выхода пользователя."""
    default_redirect_url = settings.LOGIN_URL

    def post(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(self.default_redirect_url)


class LoginView(LoginBaseView):

    """Страница входа пользователя."""
    default_redirect_url = '/'
    form_class = AuthenticationForm
    template_name = 'auth/login.html'


class LogoutView(LogoutBaseView):

    """Страница выхода пользователя."""
    default_redirect_url = '/auth/logout'   # TODO: reverse

    def get_template_names(self):
        u = self.request.user
        if u.is_authenticated():
            return ['auth/logout.html']
        return ['auth/logout_success.html']
