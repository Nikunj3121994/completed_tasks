# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


# на стадии отладки вполне подойдет
for name in (mod for mod in dict(locals()).values()):
    try:
        admin.site.register(name)
    except:
        pass
