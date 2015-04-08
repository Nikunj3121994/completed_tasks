from django.contrib.auth.backends import RemoteUserBackend
from django.conf import settings


class Krb5RemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False

    def clean_username(self, username):

        return username.rstrip(settings.KRB5_REMOTE_USER_REALM)
