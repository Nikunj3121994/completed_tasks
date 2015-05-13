# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from .base import *

DEBUG = True

# количество файлов, что может загрузить пользователь
MAX_USER_FILES_COUNT = 34
MAX_DAYS_TO_OLD = 3651

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'NAME': 'test',
    #     'USER': 'chaotism',  # 'postgres',
    #     'PASSWORD': 'herotizm',  # 'postgres',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # },
    'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }

}
