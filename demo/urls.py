# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()





urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# urlpatterns = patterns('',
#     url(r'^login/$', login),
# )

if 'angular_rest_bookmarks' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^bookmarks/', include('angular_rest_bookmarks.urls', namespace='rest_bookmarks')),
    )

if 'my_files_storage' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^my_files_storage/', include('my_files_storage.urls', namespace='my_files_storage')),
    )

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        url(r'^(?P<path>favicon\..*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.contrib.staticfiles.views.serve', dict(insecure=True)),
    )
