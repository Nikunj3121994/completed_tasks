# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import login
from django.shortcuts import redirect
from views import AuthTemplateView
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()


# urlpatterns = patterns('',
#     url(r'^$', lambda request: redirect('/auth/login')),
# )

urlpatterns = patterns('',
    url(r'^$', AuthTemplateView.as_view(template_name='welcome.html'), name='welcome'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

if 'angular_rest_bookmarks' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^bookmarks/', include('angular_rest_bookmarks.urls', namespace='rest_bookmarks')),
    )

if 'my_auth' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^auth/', include('my_auth.urls', namespace='auth')),
    )
    # from auth.urls import login_urls
    # urlpatterns += login_urls


if 'my_files_storage' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^my_files_storage/', include('my_files_storage.urls', namespace='my_files_storage')),
    )

if 'my_calculator' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^my_calculator/', include('my_calculator.urls', namespace='my_calculator')),
    )

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        url(r'^(?P<path>favicon\..*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.contrib.staticfiles.views.serve', dict(insecure=True)),
    )
