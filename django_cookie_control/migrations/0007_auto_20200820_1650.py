# Generated by Django 2.2.14 on 2020-08-20 06:50

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_cookie_control', '0006_auto_20200422_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='CCPAConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, help_text='URL where your terms may be accessed', max_length=512, null=True)),
                ('updated', models.DateField(blank=True, help_text='Terms updated date', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='back',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='configure',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='label',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='panelBack',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='vendorBack',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='vendorConfigure',
        ),
        migrations.RemoveField(
            model_name='iabtexttranslation',
            name='vendorTitle',
        ),
        migrations.RemoveField(
            model_name='textvaluetranslation',
            name='accessibilityAlert',
        ),
        migrations.AddField(
            model_name='accessibility',
            name='overlay',
            field=models.NullBooleanField(help_text='Determines if the module should use an overlay to accentuate the presence of an open notification bar or panel and discourage use of the main site while these elements are open.'),
        ),
        migrations.AddField(
            model_name='branding',
            name='rejectBackground',
            field=colorfield.fields.ColorField(blank=True, default=None, help_text="The CSS background-color that you'd like to use for the module's primary 'reject' buttons.", max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='branding',
            name='rejectText',
            field=colorfield.fields.ColorField(blank=True, default=None, help_text="The CSS color that you'd like to use for the text within the module's primary 'reject' buttons.", max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='closeOnGlobalChange',
            field=models.NullBooleanField(help_text='If set to false the Cookie Control main window will remain open when the user clicks on either of the accept or reject buttons, and the user will have to explicitly close it using the X close icon at the top right, or the close button.'),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='encodeCookie',
            field=models.NullBooleanField(help_text="If the value of Cookie Control's own cookie should be encoded as a Uniform Resource Identifier (URI)"),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='mode',
            field=models.CharField(choices=[('GDPR', 'GDPR'), ('CCPA', 'CCPA')], default='GDPR', help_text="The mode in which Cookie Control runs, either 'GDPR' or 'CCPA'", max_length=10),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='notifyDismissButton',
            field=models.NullBooleanField(help_text="Set this to false if you are using the notify interface and don't wish to show the (X) close icon on it."),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='publisherCC',
            field=models.CharField(blank=True, default='GB', help_text='Country code of the country that determines legislation of reference.', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='rejectButton',
            field=models.NullBooleanField(help_text="shows a reject button alongside the accept button on the notification bar, or alongside the 'accept recommended settings' button when the panel is open"),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='sameSiteCookie',
            field=models.NullBooleanField(help_text='Set to true the SameSite:Strict flag. Otherwise it will be flagged with SameSite:None'),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='sameSiteValue',
            field=models.CharField(blank=True, choices=[('Strict', 'Strict'), ('Lax', 'Lax'), ('None', 'None')], help_text='Used in conjuction with the sameSiteCookie property, it controls the value of the SameSite flag for the CookieControl cookie. It can be one of "Strict", "Lax" or "None"', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='settingsStyle',
            field=models.CharField(blank=True, choices=[('link', 'link'), ('button', 'button')], help_text='Determines the appearance of the settings button on the notification bar.', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='dataUse',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='features',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='panelIntro2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='panelIntro3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='purposeLegitimateInterest',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='purposes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='relyConsent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='relyLegitimateInterest',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='savePreferences',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='specialFeatures',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='specialPurposes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='vendorLegitimateInterest',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iabtexttranslation',
            name='vendors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textvaluetranslation',
            name='acceptSettings',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textvaluetranslation',
            name='cornerButton',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textvaluetranslation',
            name='landmark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textvaluetranslation',
            name='reject',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='textvaluetranslation',
            name='rejectSettings',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cookiecontrol',
            name='iabCMP',
            field=models.BooleanField(default=False, help_text='Determines whether or not Cookie Control runs as and the IAB TCF v2.0 compliant CMP.'),
        ),
        migrations.AlterField(
            model_name='cookiecontrol',
            name='layout',
            field=models.CharField(blank=True, choices=[('slideout', 'slideout'), ('popup', 'popup')], help_text='[Pro version only] Display type and behaviour of Cookie Control', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cookiecontrol',
            name='ccpaConfig',
            field=models.ForeignKey(blank=True, help_text='When in CCPA mode, use this to customise the CCPA required link name and description', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_cookie_control.CCPAConfig'),
        ),
        migrations.CreateModel(
            name='CCPAConfigTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Text introducing the privacy statement', null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='django_cookie_control.CCPAConfig')),
            ],
            options={
                'verbose_name': 'ccpa config Translation',
                'db_table': 'django_cookie_control_ccpaconfig_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]