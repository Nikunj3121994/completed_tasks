# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()





urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

if 'angular_rest_bookmarks' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^bookmarks/', include('angular_rest_bookmarks.urls', namespace='rest_bookmarks')),
    )

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        url(r'^(?P<path>favicon\..*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.contrib.staticfiles.views.serve', dict(insecure=True)),
    )
