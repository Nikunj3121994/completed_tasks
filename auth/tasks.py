# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.utils.log import get_task_logger
from django.core import management
from protokol.celery_app import app


logger = get_task_logger(__name__)


@app.task
def clear_sessions():
    logger.debug('Session cleaning')
    management.call_command('clearsessions')
