# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import (
    LoginView, LogoutView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserDetailView,
    UserBlockView, UserUnblockView, UserChangePasswordView, USER_URL_PK
)


login_urls =  patterns(
    '',
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
)

users_manage_patterns = patterns(
    '',
    url(r'^$', UserListView.as_view(), name='list'), #закоментировал остальные урлы в принципе они работают, но нужны ли тут?
    # url(r'^/(?P<%s>\d+)$' % USER_URL_PK, UserDetailView.as_view(), name='detail'),
    # url(r'^/(?P<%s>\d+)/block$' % USER_URL_PK, UserBlockView.as_view(), name='block'),
    # url(r'^/(?P<%s>\d+)/unblock$' % USER_URL_PK, UserUnblockView.as_view(), name='unblock'),
    url(r'^/add/$', UserCreateView.as_view(), name='add'),
    # url(r'^/(?P<%s>\d+)/edit$' % USER_URL_PK, UserUpdateView.as_view(), name='edit'),
    # url(r'^/(?P<%s>\d+)/delete$' % USER_URL_PK, UserDeleteView.as_view(), name='delete'),
    # url(r'^/(?P<%s>\d+)/change-password$' % USER_URL_PK, UserChangePasswordView.as_view(), name='change-password'),
    )


urlpatterns = patterns(
    '',
    url(r'^users', include(users_manage_patterns, namespace='users')),
    url(r'', include(login_urls)),
    )