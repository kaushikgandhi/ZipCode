from __future__ import absolute_import

import os
import django
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','zipcode.settings')

django.setup()

app = Celery('ziptask',backend='redis')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)