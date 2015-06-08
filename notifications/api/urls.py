# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
#from .views import MyNumberListAPIView,  MyLexemmeListAPIView, MyResultDetailView, WrongOperationView
from .views import SendEmailDetailView, EmailsListAPIView, EmailDetailView, NotificationsListAPIView, NotificationDetailView

# email_urls = patterns(
#     '',
#     url(r'^$', UsersListAPIView.as_view(), name='list'),
#     url(r'^/(?P<pk>\d+)$', UserDetail.as_view(), name='detail'),
#     url(r'^/(?P<pk>\d+)/user_(?P<type>(files|photos))$', UserFilesList.as_view(), name='userfile-list'),
#     url(r'^/(?P<pk>\d+)/user_(?P<type>(files|photos))/(?P<id>\d+)$', UserFileDetail.as_view(), name='detail'),
# )



email_urls = patterns(
    '',
    # url(r'^results/(?P<operation>(\d+\.?\d*)((\/|\+|\-|\*)(\d+\.?\d*)){1,})$', MyResultDetailView.as_view(
    # ), name='my_result'),
    # url(r'^results/\S*$', WrongOperationView.as_view(), name='my_error'),
    # url(r'^numbers$', MyNumberListAPIView.as_view(), name='my_numb'),
    # url(r'^lexemes$', MyLexemmeListAPIView.as_view(), name='my_lex'),
    url(r'^send_email/', SendEmailDetailView.as_view(
    ), name='send_email'),
    url(r'^$', EmailsListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', EmailDetailView.as_view(), name='detail'),
    # url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/users$', FileUserstList.as_view(), name='fileuser-list'),
)

notifications_urls = patterns(
    '',
    # url(r'^results/(?P<operation>(\d+\.?\d*)((\/|\+|\-|\*)(\d+\.?\d*)){1,})$', MyResultDetailView.as_view(
    # ), name='my_result'),
    # url(r'^results/\S*$', WrongOperationView.as_view(), name='my_error'),
    # url(r'^numbers$', MyNumberListAPIView.as_view(), name='my_numb'),
    # url(r'^lexemes$', MyLexemmeListAPIView.as_view(), name='my_lex'),
    # url(r'^send_email/', SendEmailDetailView.as_view(
    # ), name='send_email'),
    url(r'^$', NotificationsListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', NotificationDetailView.as_view(), name='detail'),
    # url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/users$', FileUserstList.as_view(), name='fileuser-list'),
)



# notifications_urls = patterns(
#     '',
#     url(r'^results/(?P<operation>(\d+\.?\d*)((\/|\+|\-|\*)(\d+\.?\d*)){1,})$', MyResultDetailView.as_view(
#     ), name='my_result'),
#     url(r'^results/\S*$', WrongOperationView.as_view(), name='my_error'),
#     url(r'^send_email/', SendEmailDetailView.as_view(
#     ), name='send_email'),
#     url(r'^numbers$', MyNumberListAPIView.as_view(), name='my_numb'),
#     url(r'^lexemes$', MyLexemmeListAPIView.as_view(), name='my_lex'),
# )

urlpatterns = patterns(
    '',
    url(r'^emails/', include(email_urls, namespace='emails')),
    url(r'^notifications/', include(notifications_urls, namespace='notifications')),
    # url(r'^files', include(files_urls, namespace='files')),
    # url(r'^(?P<type>(files|photos))', include(files_urls, namespace='files')),
    # url(r'^users_files', include(users_files_urls, namespace='users_files')),

)
