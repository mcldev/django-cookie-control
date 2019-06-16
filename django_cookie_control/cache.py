# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache


def _key(site_id):
    return 'django_cookie_control_{site_id}'.format(site_id=site_id)


def get(site_id):
    key = _key(site_id)
    return cache.get(key, None)


def set(site_id, cookie_control):
    key = _key(site_id)
    cache.set(key, cookie_control)


def delete(site_id):
    key = _key(site_id)
    cache.delete(key)



