# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthForm,
    SetPasswordForm as DjangoSetPasswordForm
)
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': "Такое имя пользователя уже существует.",
        'password_mismatch': "Поле пароля и подтверждения пароля не совпадают.",
    }
    password1 = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput, help_text=_("Придумайте пароль"))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput,
                                help_text=_("Повторите пароль, чтобы не ошибиться"))
                               # help_text="Enter the same password as above, for verification.")




    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['groups'].initial = self.instance.groups.all()

    # def save(self, commit=True):
    #     instance = super(UserUpdateForm, self).save(commit=True)
    #     # old_save_m2m = self.save_m2m
    #     #
    #     # def save_m2m():
    #     #     old_save_m2m()
    #     #     groups = self.cleaned_data.get('groups', [])
    #     #     inst_groups = instance.groups.all()
    #     #     add_groups = set(groups).difference(inst_groups)
    #     #     remove_groups = set(inst_groups).difference(groups)
    #     #     for group in add_groups:
    #     #         instance.groups.add(group)
    #     #     for group in remove_groups:
    #     #         instance.groups.remove(group)
    #     # self.save_m2m = save_m2m
    #     #
    #     # if commit:
    #     #     instance.save()
    #     #     self.save_m2m()
    #     return instance


class SetPasswordForm(DjangoSetPasswordForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Новый пароль еще раз'


class AuthenticationForm(DjangoAuthForm):
    error_messages = {
        'invalid_login': _("Пользователя с таким логином не обнаружено. "
                           "Внимание: логин и пароль регистрозависимы."),
        'invalid_password': _("Пожайлуста введите правильный пароль. "
                            "Внимание: логин и пароль регистрозависимы."),
        'inactive': _("Этот пользователь неактивен."),
    }

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username:
            UserModel = get_user_model()
            #print UserModel.objects.filter(username=username).exists()
            if not UserModel.objects.filter(username=username).exists():
                #print 'x'
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    #params={'username': self.username_field.verbose_name},
                )
        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_password'],
                    code='invalid_password',
                    #params={'username': self.username_field.verbose_name, 'password':self.fields['password'].label},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data
