from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from .apiviews import ZipApi
from django.contrib import admin

router = DefaultRouter(trailing_slash=False)


router.register('', ZipApi, base_name="query")


urlpatterns = patterns('',
                       url(r'api/v1', include(router.urls))
                       )