# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import (
    LoginView, LogoutView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserDetailView,
    UserBlockView, UserUnblockView, UserChangePasswordView, USER_URL_PK
)


login_urls = patterns(
    '',
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
)

users_manage_patterns = patterns(
    '',
    url(r'^$', UserListView.as_view(), name='list'),
    url(r'^/add/$', UserCreateView.as_view(), name='add'),
)


urlpatterns = patterns(
    '',
    url(r'^users', include(users_manage_patterns, namespace='users')),
    url(r'', include(login_urls)),
)
