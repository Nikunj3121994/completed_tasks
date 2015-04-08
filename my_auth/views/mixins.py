# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.decorators import REDIRECT_FIELD_NAME, login_required

#from ..choices import USER_ROLES


def roles_required(roles, raise_exception=False):
    def check_roles(user):
        if user.is_in_roles(roles):
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_roles)


def is_active_required(raise_exception=False):
    def user_is_active(user):
        if user.is_active:
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(user_is_active)


class LoginRequiredMixin(object):
    redirect_field_name = REDIRECT_FIELD_NAME
    login_url = settings.LOGIN_URL

    def dispatch(self, request, *args, **kwargs):
        return login_required(
            redirect_field_name=self.redirect_field_name,
            login_url=self.login_url)(super(LoginRequiredMixin, self).dispatch)(request, *args, **kwargs)


class IsActiveRequired(object):

    def dispatch(self, request, *args, **kwargs):
        return is_active_required(raise_exception=True)(super(IsActiveRequired, self).dispatch)(request, *args, **kwargs)


# class RolesRequiredMixin(object):
#     required_roles = []
#
#     def dispatch(self, request, *args, **kwargs):
#         return roles_required(self.get_required_roles())(super(RolesRequiredMixin, self).dispatch)(request, *args, **kwargs)
#
#     def get_required_roles(self):
#         return self.required_roles


# class AccessMixin(LoginRequiredMixin, RolesRequiredMixin):
#     user_roles = USER_ROLES


# class RolesRequiredMixin(object):
#     allow_administrator = False
#     allow_operator = False
#     allow_security_admin = False
#
#     def dispatch(self, request, *args, **kwargs):
#         return roles_required(self.get_required_roles(), raise_exception=True)(super(RolesRequiredMixin, self).dispatch)(request, *args, **kwargs)
#
#     def get_required_roles(self):
#         roles = []
#         if self.allow_administrator:
#             roles.append(USER_ROLES.ADMINISTRATOR)
#         if self.allow_operator:
#             roles.append(USER_ROLES.OPERATOR)
#         if self.allow_security_admin:
#             roles.append(USER_ROLES.SECURITY_ADMIN)
#         return roles


class AccessMixin(LoginRequiredMixin, IsActiveRequired):#, RolesRequiredMixin):
    pass

