# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django_cookie_control.settings import COOKIE_CONTROL_REQUIRED_DEFAULT

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Cookie = apps.get_model("django_cookie_control", "Cookie")
    db_alias = schema_editor.connection.alias
    for cookie in COOKIE_CONTROL_REQUIRED_DEFAULT:
        Cookie.objects.using(db_alias).create(name=cookie)


class Migration(migrations.Migration):

    dependencies = [
        ('django_cookie_control', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]