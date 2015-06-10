# -*- coding: utf-8 -*-
from celery import task
from celery.utils.log import get_task_logger

from .models import Shop

logger = get_task_logger(__name__)


@task(name='notifications.import_mailing')
def import_mailing_from_file(instance):
    shop = Shop.objects.get(instance.shop)
   # shop.update_rating()

def import_mailing_from_file_without_celery(instance):
    pass
    #raise Exception(instance)
    #shop = Shop.objects.get(instance.shop)
   # shop.update_rating()