# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from .views import MyNumberListAPIView,  MyLexemmeListAPIView, MyResultDetailView, WrongOperationView

handler404 = 'my_calculator.api.views.error404'

urlpatterns = patterns(
    '',
    url(r'^results/(?P<operation>(\d+\.?\d*)((\/|\+|\-|\*)(\d+\.?\d*)){1,})$', MyResultDetailView.as_view(
    ), name='my_result'),
    url(r'^results/\S*$', WrongOperationView.as_view(), name='my_error'),
    url(r'^numbers$', MyNumberListAPIView.as_view(), name='my_numb'),
    url(r'^lexemes$', MyLexemmeListAPIView.as_view(), name='my_lex'),
)
