# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json

from django import template

from django_cookie_control.models import CookieControl
from django_cookie_control.settings import FUNC_START_STR, FUNC_END_STR
from django_cookie_control import cache

register = template.Library()


@register.inclusion_tag("django_cookie_control/cookie-control.html", takes_context=True)
def cookie_control(context):
    request = context['request']
    site = getattr(request, 'site', None)

    cookie_control_json = cache.get(site.id)
    is_enabled = cache.get("{}_is_enabled".format(site.id))

    if not cookie_control_json:
        cookie_control = CookieControl.objects.filter(site=site).select_related('statement',
                                                                               'text',
                                                                               'accessibility',
                                                                                'branding',
                                                                                'onLoad').\
                                        prefetch_related('necessaryCookies','optionalCookies',)

        if cookie_control.exists():
            cc = cookie_control.first()
            is_enabled = cc.is_enabled
            cookie_dict = cc.get_dict()
            cookie_control_json = json.dumps(cookie_dict, indent=4, sort_keys=True)
            cookie_control_json = cookie_control_json.replace('"' + FUNC_START_STR, "").replace(FUNC_END_STR + '"', "").replace('\\"', '"')

            cache.set(site.id, cookie_control_json)
            cache.set("{}_is_enabled".format(site.id), is_enabled)

    context.update({
        'COOKIE_CONTROL_CONFIG': cookie_control_json,
        'IS_ENABLED': is_enabled,
    })

    return context

