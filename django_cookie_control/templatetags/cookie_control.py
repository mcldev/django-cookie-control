# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.safestring import mark_safe, SafeBytes

from django_cookie_control.models import CookieControl
from six.moves.urllib.parse import urlparse
import json

from django_cookie_control.settings import FUNC_START_STR, FUNC_END_STR

register = template.Library()


@register.inclusion_tag("django_cookie_control/cookie-control.html", takes_context=True)
def cookie_control(context):
    if 'request' in context:
        site_pk = get_current_site(context['request']).pk
    else:
        site_pk = settings.SITE_ID

    cookie_control = CookieControl.objects.filter(site=site_pk)
    if cookie_control.exists():
        dict = cookie_control.first().get_dict()
        dict_json = json.dumps(dict, indent=4, sort_keys=True)
        dict_json = dict_json.replace('"' + FUNC_START_STR, "").replace(FUNC_END_STR + '"', "").replace('\\"', '"')
        context['COOKIE_CONTROL_CONFIG'] = dict_json
    return context

