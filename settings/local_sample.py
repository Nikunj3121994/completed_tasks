# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from .base import *

DEBUG = True

# количество файлов, что может загрузить пользователь
MAX_USER_FILES_COUNT = 34
MAX_DAYS_TO_OLD = 365

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'completed_task',
        'USER': 'dummy',
        'PASSWORD': 'dummy',
        'HOST': 'localhost',
        'PORT': '',
    },
}
