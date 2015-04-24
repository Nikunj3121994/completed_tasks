# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from .views import MyNumberListAPIView,  MyLexemmeListAPIView, MyResultDetailView, WrongOperationView

handler404 = 'my_calculator.api.views.error404'

urlpatterns = patterns(
    '',
    # url(r'^results/\d+\.?\d*$', MyResultDetailView.as_view(), name='my_users'),
    # url(r'^results/\d+(\+\d+){1,}$', MyResultDetailView.as_view(), name='my_users'),
    # url(r'^results/((\d+)(\/|\+|\-|\*)(\d+)){1,}$', MyResultDetailView.as_view(), name='my_users'),
    url(r'^results/(?P<operation>(\d+\.?\d*)((\/|\+|\-|\*)(\d+\.?\d*)){1,})$', MyResultDetailView.as_view(), name='my_result'),
    url(r'^results/\S*$', WrongOperationView.as_view(), name='my_error'),
    url(r'^numbers$', MyNumberListAPIView.as_view(), name='my_numb'),
    url(r'^lexemes$', MyLexemmeListAPIView.as_view(), name='my_lex'),
    # url(r'^\d+', MyNumberListAPIView.as_view(), name='my_numb'),
    # url(r'^\/|\+|\-|\*', MyLeksemmaListAPIView.as_view(), name='my_lex'),
    # url(r'^comments', CommentsListAPIView.as_view(), name='comments'),
    # url(r'^likes', LikesListAPIView.as_view(), name='likes'),
    # url(r'^photos', PhotosListAPIView.as_view(), name='photos'),
)
