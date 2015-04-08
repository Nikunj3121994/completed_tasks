# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.core.exceptions import ImproperlyConfigured


class Krb5ccnameMiddleware(object):
    def process_request(self, request):
        if request.META.get('AUTH_TYPE') == 'Negotiate':
            if 'KRB5CCNAME' not in os.environ:
                try:
                    os.environ['KRB5CCNAME'] = request.META['KRB5CCNAME']
                except:
                    raise ImproperlyConfigured(
                        "The Django krb5ccname middleware requires the"
                        " kerb_auth_module (apache2) or similar is installed and configured"
                        " so that request.META['KRB5CCNAME'] is set when user agent is delegating krb5"
                        " credentials to the web server (NOTE: appopriate user agent parameters"
                        " have to be set correctly"
                        " e.g. firefox's about:config 'network.negotiate-auth.delegation-uris'"
                        " or curl --delegation always"
                        " and TGT must be forwadable (kinit -f), see klist -f for the F flag)")
