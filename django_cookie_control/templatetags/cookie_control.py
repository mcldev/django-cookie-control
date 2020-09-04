# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json

from django import template

from django_cookie_control.models import CookieControl
from django_cookie_control.settings import FUNC_START_STR, FUNC_END_STR
from django_cookie_control import cache as cookie_cache

register = template.Library()


@register.inclusion_tag("django_cookie_control/cookie-control.html", takes_context=True)
def cookie_control(context):
    request = context['request']
    site = getattr(request, 'site', None)

    cookie_dict = cookie_cache.get(site.id)

    if not cookie_dict:
        cookie_control = CookieControl.objects.filter(site=site).select_related('statement',
                                                                                'iabConfig',
                                                                                'iabText',
                                                                                'ccpaConfig',
                                                                                'text',
                                                                                'branding',
                                                                                'onLoad',
                                                                                'accessibility',
                                                                                'onLoad').\
                                        prefetch_related('necessaryCookies', 'optionalCookies',)

        if cookie_control.exists():
            # Return and Cache Cookie Object as dictionary
            cc = cookie_control.first()
            cookie_dict = cc.get_dict()
        else:
            # Return empty dictionary
            cookie_dict = {'is_enabled': False}

        # Cachce Full/Empty Dictionary - Cache Get's cleared on Model post_save
        cookie_cache.set(site.id, cookie_dict)

    cookie_control_json = ""
    if cookie_dict.get('is_enabled', False):
        cookie_control_json = json.dumps(cookie_dict, indent=4, sort_keys=True)
        cookie_control_json = cookie_control_json.replace('"' + FUNC_START_STR, "").replace(FUNC_END_STR + '"', "").replace('\\"', '"')

    context.update({
        'COOKIE_CONTROL_CONFIG': cookie_control_json,
        'instance': cookie_dict,
    })

    return context

