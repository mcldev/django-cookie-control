# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-31 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_cookie_control', '0004_auto_20190819_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='iabConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='Selected companies may access and use certain information on your device to serve relevant advertisements', help_text='Description of iabCMP', max_length=512)),
                ('globalVendorListLocation', models.CharField(default='https://vendorlist.consensu.org/vendorlist.json', help_text='Remaps the accesskey that the module is assigned to', max_length=512)),
                ('language', models.CharField(default='en', help_text='Two letter ISO language code that should be used to display information about IAB purposes.', max_length=128)),
                ('gdprAppliesGlobally', models.BooleanField(default=True, help_text='Determines whether or not consent should be obtained from all users regardless of their location')),
                ('recommendedState', models.BooleanField(default=True, help_text='Determines whether or not the 5 IAB purposes should be accepted as part of your recommended settings.')),
            ],
        ),
        migrations.CreateModel(
            name='iabText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='iabTextTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('label', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('configure', models.TextField(blank=True, null=True)),
                ('panelTitle', models.TextField(blank=True, null=True)),
                ('panelIntro', models.TextField(blank=True, null=True)),
                ('aboutIab', models.TextField(blank=True, null=True)),
                ('iabName', models.TextField(blank=True, null=True)),
                ('iabLink', models.TextField(blank=True, null=True)),
                ('panelBack', models.TextField(blank=True, null=True)),
                ('vendorTitle', models.TextField(blank=True, null=True)),
                ('vendorConfigure', models.TextField(blank=True, null=True)),
                ('vendorBack', models.TextField(blank=True, null=True)),
                ('acceptAll', models.TextField(blank=True, null=True)),
                ('rejectAll', models.TextField(blank=True, null=True)),
                ('back', models.TextField(blank=True, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='django_cookie_control.iabText')),
            ],
            options={
                'verbose_name': 'iab text Translation',
                'db_table': 'django_cookie_control_iabtext_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='iabCMP',
            field=models.BooleanField(default=False, help_text='Turns Cookie Control into an IAB registered Consent Management Provider (CMP)'),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='iabConfig',
            field=models.ForeignKey(blank=True, help_text='Cookie Control offers support for the IAB Transparency and Consent Framework (TCF v1.1), should the property iabCMP be enabled.', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_cookie_control.iabConfig'),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='iabText',
            field=models.ForeignKey(blank=True, help_text='You may also configure the text used to introduce the IAB category / panels', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_cookie_control.iabText'),
        ),
        migrations.AlterUniqueTogether(
            name='iabtexttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]