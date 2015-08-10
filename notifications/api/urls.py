# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from .views import SendEmailDetailView, EmailsListAPIView, EmailDetailView, NotificationsListAPIView, NotificationDetailView



email_urls = patterns(
    '',
    url(r'^send_email/', SendEmailDetailView.as_view(
    ), name='send_email'),
    url(r'^$', EmailsListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', EmailDetailView.as_view(), name='detail'),
)

notifications_urls = patterns(
    '',
    url(r'^$', NotificationsListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', NotificationDetailView.as_view(), name='detail'),
)



urlpatterns = patterns(
    '',
    url(r'^emails/', include(email_urls, namespace='emails')),
    url(r'^notifications/', include(notifications_urls, namespace='notifications')),
)
