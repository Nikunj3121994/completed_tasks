# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from extended_choices import Choices


USER_ROLES = Choices(
    ('OPERATOR', 1, 'Оператор'),
    ('ADMINISTRATOR', 2, 'Администратор'),
    ('SECURITY_ADMIN', 3, 'Администратор безопасности')
)
